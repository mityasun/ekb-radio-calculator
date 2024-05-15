import re
import sys
import traceback
from io import BytesIO
from io import StringIO
from typing import List, Union, Any, Dict, Type

import pandas as pd
from PIL import Image as PilImage
from PIL.Image import Resampling
from django.apps import apps
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models import Model
from django_redis import get_redis_connection

from settings.models import (City, AudioDuration, TimeInterval,
                             AudienceAge, AudienceSex, Month, WeekDay)


def clear_cache(patterns):
    """Clear Redis cache by create or updating objects."""

    cache_name = 'default'
    if settings.CACHES[cache_name][
        'BACKEND'
    ] == 'django_redis.cache.RedisCache':
        redis_conn = get_redis_connection(cache_name)
        for pattern in patterns:
            keys = redis_conn.keys(pattern)
            if keys:
                redis_conn.delete(*keys)


def generate_redis_key(self, prefix):
    """Generate key for redis cache"""

    user_id = 'anonymous'
    return f'{prefix}:{user_id}'


def to_translit(text: str) -> str:
    """
    Transliterate Cyrillic letters into Latin characters.

    Args:
        text (str): The input text containing Cyrillic characters.
    Returns:
        str: The transliterated text converted into Latin characters.
    """

    translit_dict = {
        u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd',
        u'е': 'e', u'ё': 'yo', u'ж': 'zh', u'з': 'z', u'и': 'i',
        u'й': 'y', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n',
        u'о': 'o', u'п': 'p', u'р': 'r', u'с': 's', u'т': 't',
        u'у': 'u', u'ф': 'f', u'х': 'h', u'ц': 'c', u'ч': 'ch',
        u'ш': 'sh', u'щ': 'shch', u'ъ': '', u'ы': 'y', u'ь': '',
        u'э': 'e', u'ю': 'yu', u'я': 'ya', u'j': 'j', u'q': 'q',
        u'w': 'w', u'x': 'x', u'0': '0', u'1': '1', u'2': '2',
        u'3': '3', u'4': '4', u'5': '5', u'6': '6', u'7': '7',
        u'8': '8', u'9': '9', u' ': '-'
    }

    translit_text = [translit_dict.get(c, c) for c in text.lower()]
    for item in translit_text:
        if item not in translit_dict.values():
            translit_text[translit_text.index(item)] = '-'
    translit_text = ''.join(translit_text)
    replaced_text = re.sub(r'-+', '-', translit_text.replace(' ', '-'))
    cut_text = replaced_text[:settings.NAME]
    return cut_text


def reduce_image(
        img: PilImage.Image, max_size: int, image_name: str
) -> InMemoryUploadedFile:
    """
    Reduce image to fit within a maximum size while maintaining aspect ratio.

    Args:
    - img (PilImage.Image): The input image.
    - max_size (int): The maximum size for either width or height.
    - image_name (str): The name of the image.

    Returns:
    - InMemoryUploadedFile: The reduced image file.
    """

    width, height = img.size
    if width < max_size and height < max_size:
        max_dim = max(width, height)
        if max_dim < max_size:
            ratio = max_size / max_dim
            new_width = int((float(width) * float(ratio)))
            new_height = int((float(height) * float(ratio)))
            img = img.resize((new_width, new_height), Resampling.LANCZOS)
    else:
        if width > height:
            ratio = max_size / float(width)
            new_height = int((float(height) * float(ratio)))
            img = img.resize((max_size, new_height), Resampling.LANCZOS)
        else:
            ratio = max_size / float(height)
            new_width = int((float(width) * float(ratio)))
            img = img.resize((new_width, max_size), Resampling.LANCZOS)
    output = BytesIO()
    img.save(
        output, format='JPEG', quality=settings.PHOTO_QUALITY,
        method=settings.PHOTO_RATIO
    )
    output.seek(0)
    return InMemoryUploadedFile(
        output, 'ImageField', f'{image_name}_{max_size}.jpg',
        'image/jpg', output.getbuffer().nbytes, None
    )


def normalize_phone(phone):
    """
    Normalize a given phone number to a standard format.
    Parameters:
        phone (str): The phone number to be normalized.
    Returns:
        str or None: The normalized phone number if it matches the expected
        pattern, otherwise returns None.
    """

    numbers_only = re.sub(r'\D', '', phone)
    pattern = r'^(\+?7|8)(\d{3})(\d{3})(\d{2})(\d{2})$'
    match = re.match(pattern, numbers_only)

    if match:
        groups = match.groups()
        normalized = f"+7 ({groups[1]}) {groups[2]}-{groups[3]}-{groups[4]}"
        return normalized
    else:
        return None


class ImportFromXLSX:
    """
    A class to import data from an Excel file into Django models.

    Parameters:
    - file_path (str): The path to the Excel file.

    Attributes:
    - file_path (str): The path to the Excel file.
    - radio_station_model (Django model): The RadioStation model.
    - output_buffer (StringIO): Buffer for storing output messages.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.radio_station_model = apps.get_model('stations', 'RadioStation')
        self.output_buffer = StringIO()

    @staticmethod
    def extract_int(string: str) -> Union[int, None]:
        """
        Extract numeric part from a string.

        Parameters:
        - string (str): Input string.

        Returns:
        - Union[int, None]: Extracted integer value or None if no integer
        found.
        """

        match = re.search(r'\d+', string)
        if match:
            return int(match.group())
        else:
            return None

    @staticmethod
    def decimal_to_percent(value: float) -> float:
        """
        Convert a decimal value to a percentage.

        Parameters:
        - value (float): Input decimal value.

        Returns:
        - float: Percentage value.
        """

        return round(value * 100, 2)

    @staticmethod
    def convert_to_type_or_none(
            value: Any, value_type: Any
    ) -> Union[Any, None]:
        """
        Convert a value to a specified type or None.

        Parameters:
        - value (Any): Input value.
        - value_type (Any): Desired type for conversion.

        Returns:
        - Union[Any, None]: Converted value or None if conversion fails.
        """

        if value is None or not pd.notna(value):
            return None
        try:
            if value_type == float:
                return round(value * 100, 2)
            else:
                return value_type(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def create_if_not_exists(
            objects_to_create: List[Dict[str, Any]],
            model_class: Type[Model],
            field_name: str
    ) -> None:
        """
        Create objects if they do not already exist in the database.

        Parameters:
        - objects_to_create (List[Dict[str, Any]]):
        A list of dictionaries representing the objects to create. Each
        dictionary should contain the field name and its corresponding value.
        - model_class (Type[Model]): The Django model class of the objects to
        create.
        - field_name (str): The name of the field to check for existence in
        the database.

        Returns:
        - None
        """

        existing_values = set(
            model_class.objects.values_list(field_name, flat=True)
        )
        new_objects = [
            obj for obj in objects_to_create
            if obj[field_name] not in existing_values
        ]
        if new_objects:
            objs = model_class.objects.bulk_create([
                model_class(**obj) for obj in new_objects
            ])
            print(f'Created {model_class.__name__}: {[obj for obj in objs]}')

    @staticmethod
    def create_update_mixin(
            radio_station: Type[Model],
            obj_to_create: list,
            obj_to_update: list,
            model: Type[Model],
            field: str
    ) -> None:
        """
        Helper function for bulk creation and updating of objects.

        Parameters:
        - radio_station: Radio station object.
        - obj_to_create (list): List of objects to create.
        - obj_to_update (list): List of objects to update.
        - model: Django model class.
        - field (str): Field to update.

        Returns:
        - None
        """

        with transaction.atomic():
            if obj_to_create:
                objs = model.objects.bulk_create(obj_to_create)
                print(
                    f'{radio_station}: created {model.__name__} - '
                    f'{len(objs)} pieces.'
                )
            if obj_to_update:
                objs = model.objects.bulk_update(obj_to_update, [field])
                print(
                    f'{radio_station}: updated {model.__name__} - '
                    f'{objs} times.'
                )
            elif not obj_to_create or not obj_to_update:
                print(
                    f'{radio_station}: no {model.__name__} '
                    f'objects were updated.'
                )

    def process_main_data(self, df: pd.DataFrame) -> None:
        """
        Process main data from the Excel sheet.

        Parameters:
        - df (pd.DataFrame): DataFrame with data from sheet.

        Returns:
        - None
        """

        new_months = [
            {'month': month} for month, label in Month.MONTH_LIST
        ]
        self.create_if_not_exists(new_months, Month, 'month')

        new_weekdays = [
            {'week_day': day} for day, label in WeekDay.WEEK_DAY_LIST
        ]
        self.create_if_not_exists(new_weekdays, WeekDay, 'week_day')

        time_intervals = df.iloc[1:17, 0]
        new_intervals = [
            {'time_interval': time_interval.strip()}
            for time_interval in time_intervals.astype(str).values
        ]
        self.create_if_not_exists(new_intervals, TimeInterval, 'time_interval')

        audio_durations = df.iloc[0, 1:6].tolist()
        new_durations = [
            {'audio_duration': self.extract_int(duration)}
            for duration in audio_durations
        ]
        self.create_if_not_exists(
            new_durations, AudioDuration, 'audio_duration'
        )

        block_positions = df.iloc[52, 10:22].dropna().tolist()
        block_position_model = apps.get_model('rates', 'BlockPosition')
        new_block_positions = [
            {'block_position': block_position}
            for block_position in block_positions
        ]
        self.create_if_not_exists(
            new_block_positions, block_position_model, 'block_position'
        )

    def process_stations(self, df: pd.DataFrame):
        """
        Process station data from the Excel sheet.

        Parameters:
        - df (pd.DataFrame): DataFrame with data from sheet.

        Returns:
        - None
        """

        station_data = df.iloc[19:25, 1].tolist()
        rates_data = df.iloc[50:52, 10].tolist()

        try:
            city_obj, created = City.objects.get_or_create(
                name=str(station_data[2])
            )
            if created:
                print(f'Created {City.__name__}: {city_obj}')
            defaults = {
                'city': city_obj,
                'broadcast_zone': str(station_data[3]),
                'reach_dly': self.convert_to_type_or_none(
                    station_data[4], int
                ),
                'reach_dly_percent': self.convert_to_type_or_none(
                    station_data[5], float
                ),
                'other_person_rate': round(float(rates_data[0]), 2),
                'hour_selected_rate': round(float(rates_data[1]), 2),
            }
            obj, created = self.radio_station_model.objects.get_or_create(
                name=str(station_data[0]), defaults=defaults
            )
            if created:
                print(
                    f'{obj.name}: created '
                    f'{self.radio_station_model.__name__}'
                )
            attributes_changed = any(
                getattr(obj, attr) != value for attr, value in defaults.items()
            )
            if attributes_changed:
                obj.__dict__.update(defaults)
                obj.save()
                print(
                    f'{obj.name}: updated '
                    f'{self.radio_station_model.__name__}'
                )
            else:
                print(
                    f'{obj.name}: no changes for '
                    f'{self.radio_station_model.__name__}'
                )
            return obj
        except Exception as e:
            raise RuntimeError(
                f'Error processing {self.radio_station_model.__name__} '
                f'{str(station_data[0])}: {e}'
            )

    def process_social(self, df: pd.DataFrame, station_name) -> None:
        """
        Process social data from the Excel sheet.

        Parameters:
        - df (pd.DataFrame): DataFrame with data from sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        radio_station = self.radio_station_model.objects.get(name=station_name)
        sex_data = df.iloc[25:27, 1:3]
        age_data = df.iloc[27:28, 1:3]
        social_types = [
            (
                AudienceSex,
                apps.get_model('stations', 'AudienceSexStation'),
                sex_data, 'sex'
            ),
            (
                AudienceAge,
                apps.get_model('stations', 'AudienceAgeStation'),
                age_data, 'age'
            ),
        ]
        for model1, model2, social_data, model_field in social_types:
            try:
                obj_to_update = []
                obj_to_create = []
                for index, row in social_data.iterrows():
                    string = self.convert_to_type_or_none(row[1], str)
                    percent = self.convert_to_type_or_none(row[2], float)
                    social_obj, created = model1.objects.get_or_create(
                        **{model_field: string}
                    )
                    if created:
                        print(
                            f'{radio_station}: created {model1.__name__} - '
                            f'{social_obj}'
                        )
                    obj = model2.objects.filter(
                        station=radio_station, **{model_field: social_obj}
                    ).first()
                    if obj:
                        if obj.percent == percent:
                            continue
                        obj.percent = percent
                        obj_to_update.append(obj)
                    else:
                        obj_to_create.append(
                            model2(
                                station=radio_station,
                                **{model_field: social_obj},
                                percent=percent
                            )
                        )
                self.create_update_mixin(
                    radio_station, obj_to_create, obj_to_update,
                    model2, 'percent'
                )
            except Exception as e:
                raise RuntimeError(
                    f'Error processing {model2.__name__} for '
                    f'{radio_station}: {e}'
                )

    def process_rates(self, df: pd.DataFrame, station_name) -> None:
        """
        Process rate data from the Excel sheet.

        Parameters:
        - df (pd.DataFrame): DataFrame with data from sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        radio_station = self.radio_station_model.objects.get(name=station_name)
        self.process_interval_prices(df, radio_station)
        self.process_month_rates(df, radio_station)
        self.process_block_position_rates(df, radio_station)

    def process_interval_prices(self, df: pd.DataFrame, radio_station) -> None:
        """
        Process interval price data from the Excel sheet for a given radio
        station.

        Parameters:
        - df (pd.DataFrame): DataFrame with data from sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        interval_price_model = apps.get_model('rates', 'IntervalPrice')
        try:
            price_data = df.iloc[0:17, 0:6]
            time_intervals = {
                interval.time_interval: interval for interval in
                TimeInterval.objects.all()
            }
            audio_durations = {
                duration.audio_duration: duration for duration in
                AudioDuration.objects.all()
            }
            obj_to_update = []
            obj_to_create = []
            for index, row in price_data.iloc[1:].iterrows():
                time_interval = time_intervals.get(row[0])
                for col_index in range(1, len(row)):
                    audio_duration = audio_durations.get(
                        self.extract_int(price_data.iloc[0, col_index])
                    )
                    price = row[col_index]
                    obj = interval_price_model.objects.filter(
                        station=radio_station,
                        time_interval=time_interval,
                        audio_duration=audio_duration
                    ).first()
                    if obj:
                        if obj.interval_price == price:
                            continue
                        obj.interval_price = price
                        obj_to_update.append(obj)
                    else:
                        obj_to_create.append(
                            interval_price_model(
                                station=radio_station,
                                time_interval=time_interval,
                                audio_duration=audio_duration,
                                interval_price=price,
                            )
                        )
            self.create_update_mixin(
                radio_station, obj_to_create, obj_to_update,
                interval_price_model, 'interval_price'
            )
        except RuntimeError as e:
            raise RuntimeError(
                f'Error processing {interval_price_model.__name__} for '
                f'{radio_station}: {e}'
            )

    def process_month_rates(self, df: pd.DataFrame, radio_station) -> None:
        """
        Process month rate data from the Excel sheet for a given radio station.

        Parameters:
        - df (pd.DataFrame): DataFrame with data from sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        month_rate_model = apps.get_model('rates', 'MonthRate')
        try:
            season_rates = df.iloc[48:50, 10:22]
            months = [
                month.strip().capitalize() for month in
                season_rates.iloc[0].values.tolist()
            ]
            month_rates = season_rates.iloc[1].values.tolist()
            month_objs = {
                month.month: month for month in
                Month.objects.filter(month__in=months)
            }
            obj_to_update = []
            obj_to_create = []
            for month_name, month_rate in zip(months, month_rates):
                month_obj = month_objs.get(month_name)
                obj = month_rate_model.objects.filter(
                    station=radio_station,
                    month=month_obj,
                ).first()
                if obj:
                    if obj.rate == month_rate:
                        continue
                    obj.rate = month_rate
                    obj_to_update.append(obj)
                else:
                    obj_to_create.append(
                        month_rate_model(
                            station=radio_station,
                            month=month_obj,
                            rate=month_rate
                        )
                    )
            self.create_update_mixin(
                radio_station, obj_to_create, obj_to_update,
                month_rate_model, 'rate'
            )
        except Exception as e:
            raise RuntimeError(
                f'Error processing {month_rate_model.__name__} for '
                f'{radio_station}: {e}'
            )

    def process_block_position_rates(
            self, df: pd.DataFrame, radio_station
    ) -> None:
        """
        Process block position rate data from the Excel sheet for a given
        radio station.

        Parameters:
        - df (pd.DataFrame): DataFrame with data from sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        block_position_model = apps.get_model('rates', 'BlockPosition')
        block_position_rate_model = apps.get_model(
            'rates', 'BlockPositionRate'
        )
        try:
            block_positions = df.iloc[52, 10:22].dropna().tolist()
            block_position_rates = df.iloc[53, 10:22].dropna().tolist()
            block_positions_dict = {
                block.block_position: block for block in
                block_position_model.objects.all()
            }
            obj_to_update = []
            obj_to_create = []
            for block_position, block_position_rate in zip(
                    block_positions, block_position_rates
            ):
                block_position_obj = block_positions_dict.get(block_position)
                obj = block_position_rate_model.objects.filter(
                    station=radio_station,
                    block_position=block_position_obj,
                ).first()
                if obj:
                    if obj.rate == block_position_rate:
                        continue
                    obj.rate = block_position_rate
                    obj_to_update.append(obj)
                else:
                    obj_to_create.append(
                        block_position_rate_model(
                            station=radio_station,
                            block_position=block_position_obj,
                            rate=block_position_rate
                        )
                    )
            self.create_update_mixin(
                radio_station, obj_to_create, obj_to_update,
                block_position_rate_model, 'rate'
            )
        except Exception as e:
            raise RuntimeError(
                f'Error processing {block_position_rate_model.__name__} for '
                f'{radio_station}: {e}'
            )

    def process_discounts(self, df: pd.DataFrame, station_name) -> None:
        """
        Process discount data from the Excel sheet.

        Parameters:
        - df (pd.DataFrame): DataFrame with data from sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        radio_station = self.radio_station_model.objects.get(name=station_name)

        order_amount_discount = df.iloc[2:22, 7:9]
        order_days_discount = df.iloc[23:29, 7:9]
        order_volume_discount = df.iloc[32:39, 7:9]

        discount_types = [
            (
                apps.get_model('discounts', 'AmountDiscount'),
                order_amount_discount, 'order_amount'
            ),
            (
                apps.get_model('discounts', 'DaysDiscount'),
                order_days_discount, 'total_days'
            ),
            (
                apps.get_model('discounts', 'VolumeDiscount'),
                order_volume_discount, 'order_volume'
            )
        ]

        for model, discounts_data, amount_field in discount_types:
            try:
                obj_to_update = []
                obj_to_create = []
                for index, row in discounts_data.iterrows():
                    order_value = self.convert_to_type_or_none(row[7], int)
                    order_discount = self.convert_to_type_or_none(
                        row[8], float
                    )
                    if isinstance(order_value, int) and order_value > 0:
                        obj = model.objects.filter(
                            station=radio_station,
                            **{amount_field: order_value},
                        ).first()
                        if obj:
                            if obj.discount == order_discount:
                                continue
                            obj.discount = order_discount
                            obj_to_update.append(obj)
                        else:
                            obj_to_create.append(
                                model(
                                    station=radio_station,
                                    **{amount_field: order_value},
                                    discount=order_discount
                                )
                            )
                self.create_update_mixin(
                    radio_station, obj_to_create, obj_to_update,
                    model, 'discount'
                )
            except Exception as e:
                raise RuntimeError(
                    f'Error processing {model.__name__} for '
                    f'{radio_station}: {e}'
                )

    def process_all(self) -> tuple[str, str | None] | None:
        """Returns a tuple containing:
        - Output messages (str)
        - Error message if an error occurred, otherwise None (str | None)
        If there's no data to process, returns None.
        """

        error_message = None
        try:
            sys.stdout = self.output_buffer
            df_dict = pd.read_excel(
                self.file_path, skiprows=0, nrows=55,
                sheet_name=None, header=None
            )
            sheet_names = list(df_dict.keys())
            if len(sheet_names) < 2:
                print(
                    'No additional sheets to process after the '
                    'first sheet.'
                )
                return None
            self.process_main_data(df_dict[sheet_names[1]])
            processed_stations = {}
            for sheet_name in sheet_names[1:]:
                sheet_data = df_dict[sheet_name]
                station = self.process_stations(sheet_data)
                if station and station.name:
                    processed_stations[station.name] = station
                    self.process_social(sheet_data, station)
                    self.process_rates(sheet_data, station)
                    self.process_discounts(sheet_data, station)
        except Exception as e:
            trace = traceback.format_exc()
            error_message = f'Ошибка импорта: {e}\n{trace}'
        finally:
            sys.stdout = sys.__stdout__
            output_text = self.output_buffer.getvalue()
            self.output_buffer.close()
            output_lines = output_text.split('\n')
            return '\n'.join(output_lines), error_message
