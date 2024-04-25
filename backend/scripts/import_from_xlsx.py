import math
import os
import re
from typing import List, Union, Any

import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.backend.settings_dev")
django.setup()

from discounts.models import AmountDiscount, VolumeDiscount, DaysDiscount
from rates.models import (MonthRate, BlockPosition, BlockPositionRate,
                          IntervalPrice)
from settings.models import (TimeInterval, AudioDuration, City, Month,
                             AudienceSex, AudienceAge)
from stations.models import (RadioStation, AudienceSexStation,
                             AudienceAgeStation)


class ImportFromXLSX:
    def __init__(self, file_path: str):
        self.file_path = file_path

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

    def process_stations(self, sheet_name: str) -> RadioStation:

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

            obj, created = RadioStation.objects.update_or_create(
                name=str(station_data[0]),
                defaults={
                    'title': str(station_data[0]),
                    'description': str(station_data[1]),
                    'city': city_obj,
                    'broadcast_zone': str(station_data[3]),
                    'reach_dly': reach_dly,
                    'reach_dly_percent': reach_dly_percent,
                    'other_person_rate': round(float(rates_data[0]), 2),
                    'hour_selected_rate': round(float(rates_data[1]), 2),
                }
            )
            if created:
                print(f'Created {RadioStation.__name__}: {obj.name}')
            print(f'Updated {RadioStation.__name__}: {obj.name}')
            return obj
        except Exception as e:
            print(
                f'Error processing {RadioStation.__name__}: {e}'
            )

    def process_social(
            self, sheet_name: str, station_name: RadioStation
    ) -> None:

        social_types = [
            (AudienceSex, AudienceSexStation, 'B:C', 25, 2, 'sex'),
            (AudienceAge, AudienceAgeStation, 'B:C', 27, 1, 'age'),
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
                        station=RadioStation.objects.get(name=station_name),
                        **{model_field: obj},
                        defaults={'percent': percent}
                    )
                    if created:
                        print(f'Created {model2.__name__}: {obj}')
                    print(f'Updated {model2.__name__}: {obj}')
                except Exception as e:
                    print(
                        f'Error processing {model2.__name__} '
                        f'at index {index}: {e}'
                    )

    def process_rates(
            self, sheet_name: str, station_name: RadioStation
    ) -> None:

        radio_station = RadioStation.objects.get(name=station_name)

        price_data = self.read_excel_sheet('B:F', 1, 16, sheet_name)

        time_intervals = TimeInterval.objects.all()
        audio_durations = AudioDuration.objects.all()

        for row_index, row in price_data.iterrows():
            time_interval = time_intervals[row_index]
            for col_index, price in enumerate(row):
                audio_duration = audio_durations[col_index]
                obj, created = IntervalPrice.objects.update_or_create(
                    station=radio_station,
                    time_interval=time_interval,
                    audio_duration=audio_duration,
                    defaults={'interval_price': price}
                )
                if created:
                    print(f'Created IntervalPrice: {obj}')
                else:
                    print(f'Updated IntervalPrice: {obj}')

        season_rates = self.read_excel_sheet('K:V', 48, 2, sheet_name)
        months = [
            month.strip().capitalize() for month in
            season_rates.iloc[0].values.tolist()
        ]
        month_rates = season_rates.iloc[1].values.tolist()

        for month_name, month_rate in zip(months, month_rates):
            month_obj, created = Month.objects.get_or_create(month=month_name)
            if created:
                print(f'Created {Month.__name__}: {month_obj}')
            obj, created = MonthRate.objects.update_or_create(
                station=radio_station,
                month=month_obj,
                defaults={'rate': month_rate}
            )
            if created:
                print(f'Created {MonthRate.__name__}: {obj}')
            else:
                print(f'Updated {MonthRate.__name__}: {obj}')

        block_position_rates = self.read_excel_sheet('K:V', 52, 2, sheet_name)

        block_positions = self.filter_non_nan_values(
            block_position_rates.iloc[0].values.tolist()
        )
        block_position_rates = self.filter_non_nan_values(
            block_position_rates.iloc[1].values.tolist()
        )

        for block_position, block_position_rate in zip(
                block_positions, block_position_rates
        ):
            block_position_obj, created = BlockPosition.objects.get_or_create(
                block_position=block_position
            )
            if created:
                print(f'Created {BlockPosition.__name__}: {block_position_obj}')
            obj, created = BlockPositionRate.objects.update_or_create(
                station=radio_station,
                block_position=block_position_obj,
                defaults={'rate': block_position_rate}
            )
            if created:
                print(f'Created {BlockPositionRate.__name__}: {obj}')
            else:
                print(f'Updated {BlockPositionRate.__name__}: {obj}')

    def process_discounts(
            self, sheet_name: str, station_name: RadioStation
    ) -> None:

        discount_types = [
            (AmountDiscount, 'H:I', 2, 19, 'order_amount', 'discount'),
            (DaysDiscount, 'H:I', 23, 6, 'total_days', 'discount'),
            (VolumeDiscount, 'H:I', 32, 7, 'order_volume', 'discount')
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
                            station=RadioStation.objects.get(name=station_name),
                            **{amount_field: order_value},
                            defaults={f'{discount_field}': order_discount}
                        )
                        if created:
                            print(f'Created {model.__name__}: {obj}')
                        else:
                            print(f'Updated {model.__name__}: {obj}')
                    except Exception as e:
                        print(
                            f'Error processing {model.__name__} at '
                            f'index {index}: {e}'
                        )
                else:
                    print(f'Not filled {model.__name__} {index}')

    def process_all(self):

        df_dict = pd.read_excel(self.file_path, sheet_name=None)
        sheet_names = list(df_dict.keys())
        if len(sheet_names) < 2:
            print('No additional sheets to process after the first sheet.')
            return
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


if __name__ == '__main__':

    excel_file_path = '../media/import/import.xlsx'
    assistant = ImportFromXLSX(excel_file_path)
    assistant.process_all()
