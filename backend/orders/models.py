from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from customers.models import Customer
from rates.models import BlockPosition
from settings.models import City, Month, TimeInterval, AudioDuration, WeekDay
from stations.models import RadioStation


class Order(models.Model):
    """Order model."""

    created_at = models.DateTimeField(
        'Дата и время', auto_now_add=True
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name='order_customer', verbose_name='Покупатель'
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name='order_city', verbose_name='Город'
    )
    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE,
        related_name='order_station', verbose_name='Радиостанция'
    )
    block_position = models.ForeignKey(
        BlockPosition, on_delete=models.CASCADE,
        related_name='order_block_position',
        verbose_name='Позиционирование в блоке'
    )
    block_position_rate = models.FloatField(
        'Коэффициент позиционирования в блоке',
        validators=[
            MinValueValidator(settings.MIN_PERCENT),
            MaxValueValidator(settings.MAX_PERCENT)
        ]
    )
    month = models.ForeignKey(
        Month, on_delete=models.CASCADE,
        related_name='order_month', verbose_name='Месяц'
    )
    month_rate = models.FloatField(
        'Сезонный коэффициент',
        validators=[
            MinValueValidator(settings.MIN_PERCENT),
            MaxValueValidator(settings.MAX_PERCENT)
        ]
    )
    other_person_rate = models.FloatField(
        'Коэффициент за упоминание 3-х лиц',
        validators=[
            MinValueValidator(settings.MIN_RATE),
            MaxValueValidator(settings.MAX_RATE)
        ]
    )
    hour_selected_rate = models.FloatField(
        'Коэффициент за выбор часа',
        validators=[
            MinValueValidator(settings.MIN_RATE),
            MaxValueValidator(settings.MAX_RATE)
        ]
    )
    order_amount = models.IntegerField(
        'Сумма заказа, руб.',
        validators=[
            MinValueValidator(settings.MIN_PRICE),
            MaxValueValidator(settings.MAX_PRICE)
        ]
    )
    order_amount_discount = models.FloatField(
        'Скидка за сумму заказа, %', default=settings.MIN_PERCENT,
        validators=[
            MinValueValidator(settings.MIN_PERCENT),
            MaxValueValidator(settings.MAX_PERCENT)
        ]
    )
    total_days = models.IntegerField(
        'Количество дней',
        validators=[
            MinValueValidator(settings.MIN_DAY),
            MaxValueValidator(settings.MAX_DAY)
        ]
    )
    order_days_discount = models.FloatField(
        'Скидка за продолжительность РК, %', default=settings.MIN_PERCENT,
        validators=[
            MinValueValidator(settings.MIN_PERCENT),
            MaxValueValidator(settings.MAX_PERCENT)
        ]
    )
    order_volume = models.IntegerField(
        'Количество выходов',
        validators=[
            MinValueValidator(settings.MIN_VOLUME_ORDER),
            MaxValueValidator(settings.MAX_VOLUME_ORDER)
        ]
    )
    order_volume_discount = models.FloatField(
        'Скидка за кол-во выходов в сетке, %', default=settings.MIN_PERCENT,
        validators=[
            MinValueValidator(settings.MIN_PERCENT),
            MaxValueValidator(settings.MAX_PERCENT)
        ]
    )
    final_order_amount = models.IntegerField(
        'Итого к оплате, руб.',
        validators=[
            MinValueValidator(settings.MIN_PRICE),
            MaxValueValidator(settings.MAX_PRICE)
        ]
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.id} | {self.created_at.strftime("%d.%m.%Y %H:%M")}'


class OrderCustomerSelection(models.Model):
    """Model of order customer selection."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='customer_selection_order', verbose_name='Заказ'
    )
    date = models.IntegerField(
        'Число месяца',
        validators=[
            MinValueValidator(settings.MIN_DAY),
            MaxValueValidator(settings.MAX_DAY)
        ]
    )
    week_day = models.ForeignKey(
        WeekDay, on_delete=models.CASCADE,
        related_name='customer_selection_week_day', verbose_name='День недели'
    )
    time_interval = models.ForeignKey(
        TimeInterval, on_delete=models.CASCADE,
        related_name='customer_selection_time_interval',
        verbose_name='Часовой интервал'
    )
    audio_duration = models.ForeignKey(
        AudioDuration, on_delete=models.CASCADE,
        related_name='customer_selection_audio_duration',
        verbose_name='Хронометраж ролика, сек'
    )
    interval_price = models.IntegerField(
        'Цена, руб.',
        validators=[
            MinValueValidator(settings.MIN_PRICE),
            MaxValueValidator(settings.MAX_PRICE)
        ]
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Выбор клиента'
        verbose_name_plural = 'Выбор клиента'

    def __str__(self):
        return (
            f'{self.date} | {self.week_day} | {self.time_interval} | '
            f'{self.audio_duration} | {self.interval_price}'
        )
