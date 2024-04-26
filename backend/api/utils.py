import calendar
from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (Table, TableStyle)

from settings.models import SystemText, TimeInterval, AudioDuration


def get_discount_value(queryset, ordering, attribute_name):
    """
    Helper function to retrieve a discount value from a queryset
    and handle None case.
    """

    discount_obj = queryset.order_by(ordering).first()
    return getattr(discount_obj, attribute_name) if discount_obj else 0


def get_day_name(month, day):

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


def generate_month_calendar(year, month):

    num_days = calendar.monthrange(year, month)[1]
    days_list = list(range(1, num_days + 1))
    day_names_list = [get_day_name(month, day) for day in days_list]

    return days_list, day_names_list


def create_pdf(
        city, station, month, block_position, block_position_rate,
        month_rate, other_person_rate, hour_selected_rate,
        order_amount, order_amount_discount, total_days,
        order_days_discount, order_volume, order_volume_discount,
        final_order_amount, customer_selection
):

    buffer = BytesIO()
    page = canvas.Canvas(buffer, pagesize=landscape(A4))

    pdfmetrics.registerFont(
        TTFont('Mulish-Regular', 'static/fonts/Mulish-Regular.ttf'))
    pdfmetrics.registerFont(
        TTFont('Mulish-Light', 'static/fonts/Mulish-Light.ttf'))
    pdfmetrics.registerFont(
        TTFont('Mulish-SemiBold', 'static/fonts/Mulish-SemiBold.ttf'))

    header_text = [
        f'Город: {city}',
        f'Радиостанция: {station}',
        f'Месяц: {month}',
        f'Дата составления: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
    ]

    rates_block = [
        f'Позиционирование в рекламном блоке: {block_position}',
        f'Коэффициент позиционирования в блоке: {block_position_rate}',
        f'Сезонный коэффициент: {month_rate}',
        f'Коэффициент за упоминание 3-х лиц: {other_person_rate}',
        f'Коэффициент за выбор часа: {hour_selected_rate}',
        f'Сумма заказа без скидок: {int(order_amount)} руб.',
    ]

    final_block = [
        f'Скидка за сумму заказа: {order_amount_discount}%',
        f'Продолжительность РК: {total_days} дней',
        f'Скидки за продолжительность РК: {order_days_discount}%',
        f'К-во выходов в сетке: {order_volume}',
        f'Скидка за кол-во выходов в сетке: {int(order_volume_discount)}%',
        f'Итого к оплате: {int(final_order_amount)} руб.'
    ]

    y = 510
    for line in header_text:
        page.setFont('Mulish-Regular', size=10)
        x = 30
        page.drawString(x, y, line)
        y -= 15

    y = 100
    for line in rates_block:
        page.setFont('Mulish-Regular', size=10)
        x = 30
        page.drawString(x, y, line)
        y -= 15

    y = 100
    for line in final_block:
        page.setFont('Mulish-Regular', size=10)
        x = 400
        page.drawString(x, y, line)
        y -= 15

    page.setFont('Mulish-Regular', size=6)

    days_list, day_names_list = generate_month_calendar(
        int(datetime.now().year), month.id
    )

    time_intervals = TimeInterval.objects.all().values_list(
        'time_interval', flat=True
    )

    data = [['Дата'] + days_list,
            ['Дни'] + day_names_list]

    for time_interval in time_intervals:
        row = [time_interval] + [''] * len(days_list)
        data.append(row)

    table_style = [
        ('GRID', (0, 0), (-1, -1), 1, (0.8, 0.8, 0.8)),
        ('FONTNAME', (0, 0), (-1, -1), 'Mulish-Regular'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]

    time_intervals = list(time_intervals)
    for selection in customer_selection:
        date = selection['date']
        time_interval = time_intervals[selection['time_interval'] - 1]

        audio_duration = selection['audio_duration']
        date_index = days_list.index(date) + 1
        time_interval_index = time_intervals.index(time_interval) + 2

        data[time_interval_index][date_index] = str(
            AudioDuration.objects.get(id=audio_duration))

        table_style.append(
            ('TEXTCOLOR', (date_index, time_interval_index),
             (date_index, time_interval_index), (0, 0, 0)))
        table_style.append(
            ('BACKGROUND', (date_index, time_interval_index),
             (date_index, time_interval_index),
             (185 / 255, 229 / 255, 222 / 255)))

    table = Table(data, colWidths=[1.5 * inch] + [0.3 * inch] * total_days)
    table.setStyle(TableStyle(table_style))
    table.wrapOn(page, 0, 0)
    table.drawOn(page, 30, 125)

    logo_image = ImageReader(SystemText.objects.get(pk=1).logo)
    station_logo = ImageReader(station.logo)

    original_width_1, original_height_1 = logo_image.getSize()
    max_width_1 = 200
    if original_width_1 > max_width_1:
        scale_factor_1 = max_width_1 / float(original_width_1)
        scaled_width_1 = max_width_1
        scaled_height_1 = int(original_height_1 * scale_factor_1)
    else:
        scaled_width_1 = original_width_1
        scaled_height_1 = original_height_1

    page.drawImage(logo_image, 30, 530, width=scaled_width_1,
                   height=scaled_height_1)

    company = SystemText.objects.get(pk=1)
    company_data = [
        'ООО "РА "Такса"',
        f'{company.address}',
        'ekb-radio.ru',
        f'{company.email}',
        f'{company.phone}'
    ]
    y = 560
    for line in company_data:
        page.setFont('Mulish-Regular', size=10)
        x = 330
        page.drawString(x, y, line)
        y -= 15

    original_width_2, original_height_2 = station_logo.getSize()
    max_width_2 = 150
    if original_width_2 > max_width_2:
        scale_factor_2 = max_width_2 / float(original_width_2)
        scaled_width_2 = max_width_2
        scaled_height_2 = int(original_height_2 * scale_factor_2)
    else:
        scaled_width_2 = original_width_2
        scaled_height_2 = original_height_2
    page.drawImage(station_logo, 660, 470, width=scaled_width_2,
                   height=scaled_height_2)
    page.save()
    pdf_data = buffer.getvalue()
    buffer.close()

    filename = f'Taksa_Radio_{datetime.now().strftime("%d.%m.%Y_%H.%M")}'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    response.write(pdf_data)

    return response
