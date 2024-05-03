import math
import re
from io import BytesIO
from typing import List, Union, Any

import pandas as pd
from PIL import Image as PilImage
from django.apps import apps
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404
from django_redis import get_redis_connection

from settings.models import (City, AudioDuration, TimeInterval,
                             AudienceAge, AudienceSex, Month)


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
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.radio_station_model = apps.get_model('stations', 'RadioStation')

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
            data = pd.read_excel(
                self.file_path, usecols=usecols, skiprows=skiprows,
                nrows=nrows, header=None
            )
        else:
            data = pd.read_excel(
                self.file_path, usecols=usecols, skiprows=skiprows,
                nrows=nrows, sheet_name=sheet_name, header=None
            )

        return data

    @staticmethod
    def extract_int(string: str) -> Union[int, None]:
        """regular expression to extract numeric part from the string"""

        match = re.search(r'\d+', string)
        if match:
            return int(match.group())
        else:
            return None

    @staticmethod
    def decimal_to_percent(value: float) -> float:

        return round(value * 100, 2)

    @staticmethod
    def filter_non_nan_values(lst: List) -> List:
        """Filter out None and NaN values from a list."""

        return [
            value for value in lst if value is not None and not (
                    isinstance(value, float) and math.isnan(value)
            )
        ]

    @staticmethod
    def convert_to_type_or_none(
            value: Any, value_type: Any
    ) -> Union[Any, None]:

        if value is None or not pd.notna(value):
            return None

        try:
            if value_type == float:
                return round(value * 100, 2)
            else:
                return value_type(value)
        except (ValueError, TypeError):
            return None

    def process_main_data(self, sheet_name: str) -> None:

        time_intervals = self.read_excel_sheet('A', 1, 16, sheet_name)
        for time_interval in time_intervals[0].astype(str).values:
            TimeInterval.objects.get_or_create(
                time_interval=time_interval.strip()
            )

        audio_durations = self.read_excel_sheet('B:F', 0, 1, sheet_name)
        for audio_duration in audio_durations.astype(str).values.flatten():
            AudioDuration.objects.get_or_create(
                audio_duration=self.extract_int(audio_duration)
            )

    def process_stations(self, sheet_name: str):

        station_data = (
            self.read_excel_sheet('B', 19, 6, sheet_name)
        ).values.flatten()

        rates_data = (
            self.read_excel_sheet('K', 50, 2, sheet_name)
        ).values.flatten()

        reach_dly = self.convert_to_type_or_none(station_data[4], int)
        reach_dly_percent = self.convert_to_type_or_none(station_data[5], float)

        try:
            city_obj, created = City.objects.get_or_create(
                name=str(station_data[2])
            )
            if created:
                print(f'Created {City.__name__}: {city_obj}')

            obj, created = self.radio_station_model.objects.update_or_create(
                name=str(station_data[0]),
                defaults={
                    # 'title': str(station_data[0]),
                    # 'description': str(station_data[1]),
                    'city': city_obj,
                    # 'broadcast_zone': str(station_data[3]),
                    'reach_dly': reach_dly,
                    'reach_dly_percent': reach_dly_percent,
                    'other_person_rate': round(float(rates_data[0]), 2),
                    'hour_selected_rate': round(float(rates_data[1]), 2),
                }
            )
            if created:
                print(
                    f'Created {self.radio_station_model.__name__}: {obj.name}'
                )
            print(f'Updated {self.radio_station_model.__name__}: {obj.name}')
            return obj
        except Exception as e:
            raise RuntimeError(
                f'Error processing {self.radio_station_model.__name__} '
                f'{str(station_data[0])}: {e}'
            )

    def process_social(
            self, sheet_name: str, station_name
    ) -> None:

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

        for model1, model2, usecols, skiprows, nrows, model_field in social_types:
            social_data = self.read_excel_sheet(
                usecols, skiprows, nrows, sheet_name
            )
            for index, row in social_data.iterrows():
                string = self.convert_to_type_or_none(row[1], str)
                percent = self.convert_to_type_or_none(row[2], float)

                try:
                    obj, created = model1.objects.get_or_create(
                        **{model_field: string}
                    )
                    if created:
                        print(f'Created {model1.__name__}: {obj}')
                    obj, created = model2.objects.update_or_create(
                        station=self.radio_station_model.objects.get(
                            name=station_name
                        ),
                        **{model_field: obj},
                        defaults={'percent': percent}
                    )
                    if created:
                        print(f'Created {model2.__name__}: {obj}')
                    print(f'Updated {model2.__name__}: {obj}')
                except Exception as e:
                    raise RuntimeError(
                        f'Error processing {model2.__name__} {station_name} '
                        f'in string {string}: {e}'
                    )

    def process_rates(
            self, sheet_name: str, station_name
    ) -> None:

        radio_station = self.radio_station_model.objects.get(name=station_name)

        price_data = self.read_excel_sheet('B:F', 1, 16, sheet_name)

        try:
            time_intervals = TimeInterval.objects.all()
            audio_durations = AudioDuration.objects.all()
            interval_price_model = apps.get_model('rates', 'IntervalPrice')
            for row_index, row in price_data.iterrows():
                time_interval = time_intervals[row_index]
                for col_index, price in enumerate(row):
                    audio_duration = audio_durations[col_index]
                    obj, created = interval_price_model.objects.update_or_create(
                        station=radio_station,
                        time_interval=time_interval,
                        audio_duration=audio_duration,
                        defaults={'interval_price': price}
                    )
                    if created:
                        print(f'Created IntervalPrice: {obj}')
                    else:
                        print(f'Updated IntervalPrice: {obj}')
        except Exception as e:
            raise RuntimeError(
                f'Error processing IntervalPrice {radio_station}: {e}'
            )

        try:
            season_rates = self.read_excel_sheet('K:V', 48, 2, sheet_name)
            months = [
                month.strip().capitalize() for month in
                season_rates.iloc[0].values.tolist()
            ]
            month_rates = season_rates.iloc[1].values.tolist()
            month_rate_model = apps.get_model('rates', 'MonthRate')
            for month_name, month_rate in zip(months, month_rates):
                month_obj = get_object_or_404(Month, month=month_name)
                obj, created = month_rate_model.objects.update_or_create(
                    station=radio_station,
                    month=month_obj,
                    defaults={'rate': month_rate}
                )
                if created:
                    print(f'Created {month_rate_model.__name__}: {obj}')
                else:
                    print(f'Updated {month_rate_model.__name__}: {obj}')
        except Exception as e:
            raise RuntimeError(
                f'Error processing MontRate {radio_station}: {e}'
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

            block_position_model = apps.get_model('rates', 'BlockPosition')
            block_position_rate_model = apps.get_model(
                'rates', 'BlockPositionRate'
            )

            for block_position, block_position_rate in zip(
                    block_positions, block_position_rates
            ):
                block_position_obj, created = block_position_model.objects.get_or_create(
                    block_position=block_position
                )
                if created:
                    print(
                        f'Created {block_position_model.__name__}: '
                        f'{block_position_obj}'
                    )
                obj, created = block_position_rate_model.objects.update_or_create(
                    station=radio_station,
                    block_position=block_position_obj,
                    defaults={'rate': block_position_rate}
                )
                if created:
                    print(
                        f'Created {block_position_rate_model.__name__}: {obj}'
                    )
                else:
                    print(
                        f'Updated {block_position_rate_model.__name__}: {obj}'
                    )
        except Exception as e:
            raise RuntimeError(
                f'Error processing BlockPositionRate {radio_station}: {e}'
            )

    def process_discounts(
            self, sheet_name: str, station_name
    ) -> None:

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

        for model, usecols, skiprows, nrows, amount_field, discount_field in discount_types:
            discounts_data = self.read_excel_sheet(
                usecols, skiprows, nrows, sheet_name
            )
            for index, row in discounts_data.iterrows():
                order_value = self.convert_to_type_or_none(row[7], int)
                order_discount = self.convert_to_type_or_none(row[8], float)

                if isinstance(order_value, int) and order_value > 0:
                    try:
                        obj, created = model.objects.update_or_create(
                            station=self.radio_station_model.objects.get(
                                name=station_name
                            ),
                            **{amount_field: order_value},
                            defaults={f'{discount_field}': order_discount}
                        )
                        if created:
                            print(f'Created {model.__name__}: {obj}')
                        else:
                            print(f'Updated {model.__name__}: {obj}')
                    except Exception as e:
                        raise RuntimeError(
                            f'Error processing {model.__name__} station_name '
                            f'in string {row}: {e}'
                        )
                else:
                    print(f'Not filled {model.__name__} {index}')

    def process_all(self):

        try:
            df_dict = pd.read_excel(self.file_path, sheet_name=None)
            sheet_names = list(df_dict.keys())
            if len(sheet_names) < 2:
                print('No additional sheets to process after the first sheet.')
                return
            remaining_sheet_names = sheet_names[1:]
            # self.process_main_data(sheet_names[1])
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
