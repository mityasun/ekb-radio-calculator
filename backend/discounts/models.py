from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from stations.models import RadioStation


class AbstractDiscountStation(models.Model):
    """Abstract model for discounts of station."""

    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE, verbose_name='Радиостанция'
    )
    discount = models.FloatField(
        'Скидка, %', blank=True, null=True,
        validators=[
            MinValueValidator(settings.MIN_PERCENT),
            MaxValueValidator(settings.MAX_PERCENT)
        ]
    )

    class Meta:
        abstract = True


class AmountDiscount(AbstractDiscountStation):
    """Order amount discount model."""

    order_amount = models.IntegerField(
        'Сумма заказа, руб.', blank=True, null=True,
        validators=[
            MinValueValidator(settings.MIN_PRICE),
            MaxValueValidator(settings.MAX_PRICE)
        ]
    )

    class Meta:
        verbose_name = 'Скидка за сумму заказа, %'
        verbose_name_plural = 'Скидки за сумму заказа, %'
        constraints = [
            models.UniqueConstraint(
                fields=['order_amount', 'station'], name='%(class)s_unique'
            )
        ]

    def __str__(self):
        return f'{self.station} | {self.order_amount} | {self.discount}'


class DaysDiscount(AbstractDiscountStation):
    """Order days discount model."""

    total_days = models.IntegerField(
        'Количество дней', blank=True, null=True,
        validators=[
            MinValueValidator(settings.MIN_DAY),
            MaxValueValidator(settings.MAX_DAY)
        ]
    )

    class Meta:
        verbose_name = 'Скидка за продолжительность РК, %'
        verbose_name_plural = 'Скидки за продолжительность РК, %'
        constraints = [
            models.UniqueConstraint(
                fields=['total_days', 'station'], name='%(class)s_unique'
            )
        ]

    def __str__(self):
        return f'{self.station} | {self.total_days} | {self.discount}'


class VolumeDiscount(AbstractDiscountStation):
    """Order volume discount model."""

    order_volume = models.IntegerField(
        'Количество выходов', blank=True, null=True,
        validators=[
            MinValueValidator(settings.MIN_VOLUME_ORDER),
            MaxValueValidator(settings.MAX_VOLUME_ORDER)
        ]
    )

    class Meta:
        verbose_name = 'Скидка за кол-во выходов в сетке, %'
        verbose_name_plural = 'Скидки за кол-во выходов в сетке, %'
        constraints = [
            models.UniqueConstraint(
                fields=['order_volume', 'station'], name='%(class)s_unique'
            )
        ]

    def __str__(self):
        return f'{self.station} | {self.order_volume} | {self.discount}'
