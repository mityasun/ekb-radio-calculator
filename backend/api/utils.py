import calendar
from datetime import datetime
from io import BytesIO
from typing import List, Tuple, Any

from django.db.models import QuerySet
from django.http import HttpResponse
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from rates.models import BlockPosition
from settings.models import SystemText, TimeInterval, AudioDuration, City, Month
from stations.models import RadioStation


def get_discount_value(
        queryset: QuerySet, ordering: str, attribute_name: str
) -> Any:
    """
    Helper function to retrieve a discount value from a queryset
    and handle None case.

    Parameters:
    - queryset: Django QuerySet object
    - ordering: String representing the field to order the queryset
    - attribute_name: String representing the name of the attribute to retrieve

    Returns:
    - The value of the specified attribute from the first object in the ordered
    queryset, or 0 if the queryset is empty or if the attribute value is None.
    """

    discount_obj = queryset.order_by(ordering).first()
    return getattr(discount_obj, attribute_name) if discount_obj else 0


def scaling_image(image: ImageReader, max_width: int) -> Tuple[int, int]:
    """
    Scales the given image proportionally based on the maximum width.

    Parameters:
    - image: ImageReader object
    - max_width: Maximum width for the image

    Returns:
    - scaled_width: Width of the scaled image
    - scaled_height: Height of the scaled image
    """

    original_width, original_height = image.getSize()
    if original_width > max_width:
        scale_factor = max_width / float(original_width)
        scaled_width = max_width
        scaled_height = int(original_height * scale_factor)
    else:
        scaled_width = original_width
        scaled_height = original_height
    return scaled_width, scaled_height


def draw_lines(
        start_y: int, start_x: int, offset_y: int,
        page: canvas.Canvas, text: list
):
    """
    Draws lines of text on the page starting from the specified coordinates.

    Parameters:
    - start_y: Starting y-coordinate
    - start_x: Starting x-coordinate
    - offset_y: Offset between lines
    - page: Canvas object
    - text: List of text lines to draw
    """

    y = start_y
    for line in text:
        x = start_x
        page.drawString(x, y, line)
        y -= offset_y


def get_day_name(month: int, day: int) -> str:
    """
    Gets the abbreviated name of the day for the given month and day.

    Parameters:
    - month: Month (integer)
    - day: Day of the month (integer)

    Returns:
    - Abbreviated day name (e.g., 'ПН' for Monday)
    """

    date_obj = datetime(datetime.now().year, month, day)
    day_name = date_obj.strftime('%A')
    day_name_map = {
        'Monday': 'ПН',
        'Tuesday': 'ВТ',
        'Wednesday': 'СР',
        'Thursday': 'ЧТ',
        'Friday': 'ПТ',
        'Saturday': 'СБ',
        'Sunday': 'ВС'
    }
    return day_name_map.get(day_name, '')


def generate_month_calendar(
        year: int, month: int
) -> Tuple[List[int], List[str]]:
    """
    Generates lists of day numbers and abbreviated day names for a given month.

    Parameters:
    - year: Year (integer)
    - month: Month (integer)

    Returns:
    - days_list: List of day numbers
    - day_names_list: List of abbreviated day names
    """

    num_days = calendar.monthrange(year, month)[1]
    days_list = list(range(1, num_days + 1))
    day_names_list = [get_day_name(month, day) for day in days_list]

    return days_list, day_names_list


def is_weekend(day: int, month: int) -> bool:
    """
    Checks if the given day falls on a weekend (Saturday or Sunday)
    for the specified month.

    Parameters:
    - day: Day of the month (integer)
    - month: Month (integer)

    Returns:
    - True if the day is a weekend, False otherwise
    """

    weekday = calendar.weekday(datetime.now().year, month, day)
    return weekday == 5 or weekday == 6


def create_pdf(
        city: City, station: RadioStation, month: Month,
        block_position: BlockPosition,
        block_position_rate: float, month_rate: float,
        other_person_rate: float,
        hour_selected_rate: float, order_amount: float,
        order_amount_discount: float,
        total_days: int, order_days_discount: float, order_volume: float,
        order_volume_discount: float, final_order_amount: float,
        customer_selection: list
) -> HttpResponse:
    """
    Generates a PDF document based on provided data.

    Parameters:
    - city: City objects
    - station: RadioStation objects
    - month: Month objects
    - block_position: BlockPosition objects
    - block_position_rate: Rate for block position (float)
    - month_rate: Seasonal rate (float)
    - other_person_rate: Rate for mentioning other people (float)
    - hour_selected_rate: Rate for selected hour (float)
    - order_amount: Total order amount (float)
    - order_amount_discount: Discount percentage for order amount (float)
    - total_days: Total number of days for the campaign (integer)
    - order_days_discount: Discount percentage for campaign duration (float)
    - order_volume: Total volume of the order (float)
    - order_volume_discount: Discount percentage for order volume (float)
    - final_order_amount: Final amount to be paid (float)
    - customer_selection: List of dictionaries representing customer selections

    Returns:
    - response: HttpResponse object containing the generated PDF document
    """

    buffer = BytesIO()
    page = canvas.Canvas(buffer, pagesize=landscape(A4))

    pdfmetrics.registerFont(
        TTFont('Mulish-Regular', 'static/fonts/Mulish-Regular.ttf')
    )
    pdfmetrics.registerFont(
        TTFont('Mulish-Light', 'static/fonts/Mulish-Light.ttf')
    )
    pdfmetrics.registerFont(
        TTFont('Mulish-SemiBold', 'static/fonts/Mulish-SemiBold.ttf')
    )

    page.setFont('Mulish-Regular', size=10)

    logo_image = ImageReader(SystemText.objects.get(pk=1).logo)
    scaled_width, scaled_height = scaling_image(logo_image, 200)
    page.drawImage(
        logo_image, 30, 530, width=scaled_width, height=scaled_height
    )
    station_logo = ImageReader(station.logo)
    scaled_width, scaled_height = scaling_image(station_logo, 150)
    page.drawImage(
        station_logo, 660, 470, width=scaled_width, height=scaled_height
    )

    company = SystemText.objects.get(pk=1)
    company_data = [
        'ООО "РА "Такса"',
        f'{company.address}',
        'ekbradio.ru',
        f'{company.email}',
        f'{company.phone}'
    ]
    draw_lines(560, 330, 15, page, company_data)

    header_text = [
        f'Город: {city}',
        f'Радиостанция: {station}',
        f'Месяц: {month}',
        f'Дата составления: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
    ]
    draw_lines(510, 30, 15, page, header_text)

    days_list, day_names_list = generate_month_calendar(
        int(datetime.now().year), month.id
    )
    time_intervals = TimeInterval.objects.all().values_list(
        'time_interval', flat=True
    )
    data = [
        ['Дата'] + days_list, ['Интервалы'] + day_names_list
    ]

    for time_interval in time_intervals:
        row = [time_interval] + [''] * len(days_list)
        data.append(row)

    table_style = [
        ('GRID', (0, 0), (-1, -1), 1, (0.8, 0.8, 0.8)),
        ('FONTNAME', (0, 0), (-1, -1), 'Mulish-Regular'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]

    for i, day in enumerate(days_list, start=1):
        if is_weekend(day, month.id):
            table_style.append(
                ('BACKGROUND', (i, 0), (i, -1), HexColor('#BBEDDA'))
            )

    time_intervals = list(time_intervals)
    for selection in customer_selection:
        date = selection['date']
        time_interval = time_intervals[selection['time_interval'] - 1]
        audio_duration = selection['audio_duration']
        date_index = days_list.index(date) + 1
        time_interval_index = time_intervals.index(time_interval) + 2
        data[time_interval_index][date_index] = str(
            AudioDuration.objects.get(id=audio_duration)
        )
        table_style.append(
            ('TEXTCOLOR', (date_index, time_interval_index),
             (date_index, time_interval_index), HexColor('#000')))
        table_style.append(
            ('BACKGROUND', (date_index, time_interval_index),
             (date_index, time_interval_index), HexColor('#05BB75'))
        )

    table = Table(data, colWidths=[1.5 * inch] + [0.3 * inch] * total_days)
    table.setStyle(TableStyle(table_style))
    table.wrapOn(page, 0, 0)
    table.drawOn(page, 30, 125)

    rates_block = [
        f'Позиционирование в рекламном блоке: {block_position}',
        f'Коэффициент позиционирования в блоке: {block_position_rate}',
        f'Сезонный коэффициент: {month_rate}',
        f'Коэффициент за упоминание 3-х лиц: {other_person_rate}',
        f'Коэффициент за выбор часа: {hour_selected_rate}',
        f'Сумма заказа без скидок: {
            '{:,}'.format(int(order_amount)).replace(',', ' ')
        } руб.',
    ]
    draw_lines(100, 30, 15, page, rates_block)

    final_block = [
        f'Скидка за сумму заказа: {order_amount_discount}%',
        f'Продолжительность рекламной кампании: {total_days} дней',
        f'Скидка за продолжительность рекламной кампании: '
        f'{order_days_discount}%',
        f'Количество выходов в сетке: {order_volume}',
        f'Скидка за количество выходов в сетке: {int(order_volume_discount)}%',
        f'Итого к оплате: {
            '{:,}'.format(int(final_order_amount)).replace(',', ' ')
        } руб.'
    ]
    draw_lines(100, 400, 15, page, final_block)

    page.save()
    pdf_data = buffer.getvalue()
    buffer.close()

    filename = f'Taksa_Radio_{datetime.now().strftime("%d.%m.%Y_%H.%M")}'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    response.write(pdf_data)

    return response
