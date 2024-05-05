import math
import re
import sys
from io import BytesIO
from io import StringIO
from typing import List, Union, Any

import pandas as pd
from PIL import Image as PilImage
from django.apps import apps
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_redis import get_redis_connection

from settings.models import (City, AudioDuration, TimeInterval,
                             AudienceAge, AudienceSex, Month, WeekDay)


def clear_cache(patterns):
    """Clear Redis cache by create or updating objects."""

    cache_name = 'default'
    if settings.CACHES[cache_name]['BACKEND'] == 'django_redis.cache.RedisCache':
        redis_conn = get_redis_connection(cache_name)
        for pattern in patterns:
            keys = redis_conn.keys(pattern)
            if keys:
                redis_conn.delete(*keys)


def generate_redis_key(self, prefix):
    """Generate key for redis cache"""

    user_id = 'anonymous'

    return f'{prefix}:{user_id}'


def to_translit(text):
    """Translator cyrillic letters into Latin."""

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
    slug = re.sub(r'[-]+', '-', translit_text.replace(' ', '-'))
    cut_slug = slug[:settings.NAME]
    return cut_slug


def reduce_image(img, max_size, image_name):
    """Reduce image to different sizes with minimum size requirement."""

    width, height = img.size
    if width < max_size and height < max_size:
        max_dim = max(width, height)
        if max_dim < max_size:
            ratio = max_size / max_dim
            new_width = int((float(width) * float(ratio)))
            new_height = int((float(height) * float(ratio)))
            img = img.resize((new_width, new_height), PilImage.LANCZOS)
    else:
        if width > height:
            ratio = max_size / float(width)
            new_height = int((float(height) * float(ratio)))
            img = img.resize((max_size, new_height), PilImage.LANCZOS)
        else:
            ratio = max_size / float(height)
            new_width = int((float(width) * float(ratio)))
            img = img.resize((new_width, max_size), PilImage.LANCZOS)
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

    def read_excel_sheet(
            self, usecols, skiprows: int, nrows: int, sheet_name=None
    ) -> pd.DataFrame:
        """
        Read data from an Excel sheet with optional sheet name.

        Parameters:
        - usecols (str or list-like): Columns to read.
        - skiprows (int or list-like): Rows to skip from the beginning.
        - nrows (int): Number of rows to read.
        - sheet_name (str, optional): Name of the sheet to read.
        Defaults to None (reads the first sheet).

        Returns:
        - pd.DataFrame: DataFrame containing the read data.
        """

        if sheet_name is None:
            return pd.read_excel(
                self.file_path, usecols=usecols, skiprows=skiprows,
                nrows=nrows, header=None
            )
        else:
            return pd.read_excel(
                self.file_path, usecols=usecols, skiprows=skiprows,
                nrows=nrows, sheet_name=sheet_name, header=None
            )

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
    def filter_non_nan_values(lst: List) -> List:
        """
        Filter out None and NaN values from a list.

        Parameters:
        - lst (List): Input list.

        Returns:
        - List: Filtered list without None and NaN values.
        """

        return [
            value for value in lst if value is not None and not (
                isinstance(value, float) and math.isnan(value)
            )
        ]

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
    def create_update_mixin(
            radio_station,
            obj_to_create: list,
            obj_to_update: list,
            model,
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

    def process_main_data(self, sheet_name: str) -> None:
        """
        Process main data from the Excel sheet.

        Parameters:
        - sheet_name (str): Name of the sheet.

        Returns:
        - None
        """

        months_data = self.read_excel_sheet('K:V', 48, 1, sheet_name)
        existing_months = set(Month.objects.values_list('month', flat=True))
        new_months = [
            month.strip().capitalize()
            for month in months_data.astype(str).values.flatten()
            if month.strip().capitalize() not in existing_months
        ]
        if new_months:
            objs = Month.objects.bulk_create([
                Month(month=month) for month in new_months
            ])
            print(f'Created {Month.__name__}: {[obj.month for obj in objs]}')

        existing_weekdays = set(
            WeekDay.objects.values_list('week_day', flat=True)
        )
        new_weekdays = [
            day for day, label in WeekDay.WEEK_DAY_LIST
            if day not in existing_weekdays
        ]
        if new_weekdays:
            objs = WeekDay.objects.bulk_create([
                WeekDay(week_day=day) for day in new_weekdays
            ])
            print(
                f'Created {WeekDay.__name__}: {[obj.week_day for obj in objs]}'
            )

        time_intervals = self.read_excel_sheet('A', 1, 16, sheet_name)
        existing_intervals = set(
            TimeInterval.objects.values_list('time_interval', flat=True)
        )
        new_intervals = [
            TimeInterval(time_interval=time_interval.strip())
            for time_interval in time_intervals[0].astype(str).values
            if time_interval.strip() not in existing_intervals
        ]
        if new_intervals:
            objs = TimeInterval.objects.bulk_create(new_intervals)
            print(
                f'Created {TimeInterval.__name__}: '
                f'{[obj.time_interval for obj in objs]}'
            )

        audio_durations = self.read_excel_sheet('B:F', 0, 1, sheet_name)
        existing_durations = set(
            AudioDuration.objects.values_list('audio_duration', flat=True)
        )
        new_durations = [
            self.extract_int(audio_duration)
            for audio_duration in audio_durations.astype(str).values.flatten()
            if self.extract_int(audio_duration) not in existing_durations
        ]
        if new_durations:
            objs = AudioDuration.objects.bulk_create([
                AudioDuration(audio_duration=duration)
                for duration in new_durations
            ])
            print(
                f'Created {AudioDuration.__name__}: '
                f'{[obj.audio_duration for obj in objs]}'
            )

    def process_stations(self, sheet_name: str):
        """
        Process station data from the Excel sheet.

        Parameters:
        - sheet_name (str): Name of the sheet.

        Returns:
        - None
        """

        station_data = (
            self.read_excel_sheet('B', 19, 6, sheet_name)
        ).values.flatten()

        rates_data = (
            self.read_excel_sheet('K', 50, 2, sheet_name)
        ).values.flatten()

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
            attributes_changed = any(
                getattr(obj, attr) != value for attr, value in defaults.items()
            )
            if attributes_changed:
                obj.__dict__.update(defaults)
                obj.save()
                if created:
                    print(
                        f'{obj.name}: created '
                        f'{self.radio_station_model.__name__}'
                    )
                else:
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

    def process_social(self, sheet_name: str, station_name) -> None:
        """
        Process social data from the Excel sheet.

        Parameters:
        - sheet_name (str): Name of the sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        radio_station = self.radio_station_model.objects.get(name=station_name)
        social_types = [
            (
                AudienceSex,
                apps.get_model('stations', 'AudienceSexStation'),
                'B:C', 25, 2, 'sex'
            ),
            (
                AudienceAge,
                apps.get_model('stations', 'AudienceAgeStation'),
                'B:C', 27, 1, 'age'
            ),
        ]
        for (
                model1, model2, usecols, skiprows, nrows, model_field
        ) in social_types:
            social_data = self.read_excel_sheet(
                usecols, skiprows, nrows, sheet_name
            )
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

    def process_rates(self, sheet_name: str, station_name) -> None:
        """
        Process rate data from the Excel sheet.

        Parameters:
        - sheet_name (str): Name of the sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        radio_station = self.radio_station_model.objects.get(name=station_name)
        self.process_interval_prices(sheet_name, radio_station)
        self.process_month_rates(sheet_name, radio_station)
        self.process_block_position_rates(sheet_name, radio_station)

    def process_interval_prices(self, sheet_name: str, radio_station) -> None:
        """
        Process interval price data from the Excel sheet for a given radio
        station.

        Parameters:
        - sheet_name (str): Name of the sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        interval_price_model = apps.get_model('rates', 'IntervalPrice')
        try:
            price_data = self.read_excel_sheet('B:F', 1, 16, sheet_name)
            time_intervals = TimeInterval.objects.all()
            audio_durations = AudioDuration.objects.all()
            obj_to_update = []
            obj_to_create = []
            for row_index, row in price_data.iterrows():
                time_interval = time_intervals[row_index]
                for col_index, price in enumerate(row):
                    audio_duration = audio_durations[col_index]
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

    def process_month_rates(self, sheet_name: str, radio_station) -> None:
        """
        Process month rate data from the Excel sheet for a given radio station.

        Parameters:
        - sheet_name (str): Name of the sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        month_rate_model = apps.get_model('rates', 'MonthRate')
        try:
            season_rates = self.read_excel_sheet('K:V', 48, 2, sheet_name)
            months = [
                month.strip().capitalize() for month in
                season_rates.iloc[0].values.tolist()
            ]
            month_rates = season_rates.iloc[1].values.tolist()
            obj_to_update = []
            obj_to_create = []
            for month_name, month_rate in zip(months, month_rates):
                month_obj = get_object_or_404(Month, month=month_name)
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
            self, sheet_name: str, radio_station
    ) -> None:
        """
        Process block position rate data from the Excel sheet for a given
        radio station.

        Parameters:
        - sheet_name (str): Name of the sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        block_position_model = apps.get_model('rates', 'BlockPosition')
        block_position_rate_model = apps.get_model(
            'rates', 'BlockPositionRate'
        )
        try:
            block_position_rates = self.read_excel_sheet(
                'K:V', 52, 2, sheet_name
            )
            block_positions = self.filter_non_nan_values(
                block_position_rates.iloc[0].values.tolist()
            )
            block_position_rates = self.filter_non_nan_values(
                block_position_rates.iloc[1].values.tolist()
            )
            obj_to_update = []
            obj_to_create = []
            for block_position, block_position_rate in zip(
                    block_positions, block_position_rates
            ):
                block_position_obj, created = block_position_model.objects.get_or_create(
                    block_position=block_position
                )
                if created:
                    print(
                        f'{radio_station}: created '
                        f'{block_position_model.__name__} - '
                        f'{block_position_obj}'
                    )
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

    def process_discounts(self, sheet_name: str, station_name) -> None:
        """
        Process discount data from the Excel sheet.

        Parameters:
        - sheet_name (str): Name of the sheet.
        - station_name: Name of the station.

        Returns:
        - None
        """

        radio_station = self.radio_station_model.objects.get(name=station_name)

        discount_types = [
            (
                apps.get_model('discounts', 'AmountDiscount'),
                'H:I', 2, 19, 'order_amount', 'discount'
            ),
            (
                apps.get_model('discounts', 'DaysDiscount'),
                'H:I', 23, 6, 'total_days', 'discount'
            ),
            (
                apps.get_model('discounts', 'VolumeDiscount'),
                'H:I', 32, 7, 'order_volume', 'discount'
            )
        ]

        for (
                model, usecols, skiprows, nrows, amount_field, discount_field
        ) in discount_types:
            discounts_data = self.read_excel_sheet(
                usecols, skiprows, nrows, sheet_name
            )
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

    def process_all(self) -> Union[str, None]:
        """
        Process all data from the Excel file.

        Returns:
        - Union[str, None]: Output messages or None if no data to process.
        """

        try:
            sys.stdout = self.output_buffer
            df_dict = pd.read_excel(self.file_path, sheet_name=None)
            sheet_names = list(df_dict.keys())
            if len(sheet_names) < 2:
                print(
                    'No additional sheets to process after the '
                    'first sheet.'
                )
                return None
            remaining_sheet_names = sheet_names[1:]
            self.process_main_data(sheet_names[1])
            processed_stations = {}
            for sheet_name in remaining_sheet_names:
                station = self.process_stations(sheet_name)
                if station and station.name:
                    processed_stations[station.name] = station
                    self.process_social(sheet_name, station)
                    self.process_rates(sheet_name, station)
                    self.process_discounts(sheet_name, station)
        except Exception as e:
            raise RuntimeError(f'Ошибка импорта: {e}')
        finally:
            sys.stdout = sys.__stdout__
            output_text = self.output_buffer.getvalue()
            self.output_buffer.close()
            output_lines = output_text.split('\n')
            return '\n'.join(output_lines)
