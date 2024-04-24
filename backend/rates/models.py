from functools import partial

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from settings.models import Month, TimeInterval, AudioDuration
from stations.models import RadioStation
from utils.abstract_models import DefaultOneMixin
from utils.validators import validate_text


class AbstractRateStation(models.Model):
    """Abstract model for rates of station."""

    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE, verbose_name='Радиостанция'
    )
    rate = models.FloatField(
        'Коэффициент', validators=[
            MinValueValidator(settings.MIN_PERCENT),
            MaxValueValidator(settings.MAX_PERCENT)
        ]
    )

    class Meta:
        abstract = True


class MonthRate(AbstractRateStation):
    """Month rate model."""

    month = models.ForeignKey(
        Month, on_delete=models.CASCADE, verbose_name='Месяц'
    )

    class Meta:
        verbose_name = 'Сезонный коэффициент'
        verbose_name_plural = 'Сезонные коэффициенты'
        constraints = [
            models.UniqueConstraint(
                fields=['station', 'month'], name='%(class)s_unique'
            )
        ]

    def __str__(self):
        return f'{self.station} | {self.month} | {self.rate}'


class BlockPosition(DefaultOneMixin, models.Model):
    """Block position model."""

    block_position = models.CharField(
        'Позиционирование в блоке',
        max_length=settings.NAME, unique=True,
        validators=[partial(validate_text, max_length=settings.NAME)]
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Позиционирование в блоке'
        verbose_name_plural = 'Позиционирование в блоке'

    def __str__(self):
        return f'{self.block_position}'


class BlockPositionRate(AbstractRateStation):
    """Block position rate model."""

    block_position = models.ForeignKey(
        BlockPosition, on_delete=models.CASCADE,
        verbose_name='Позиционирование в блоке'
    )

    class Meta:
        verbose_name = 'Коэффициент позиционирования в блоке'
        verbose_name_plural = 'Коэффициент позиционирования в блоке'
        constraints = [
            models.UniqueConstraint(
                fields=['station', 'block_position'], name='%(class)s_unique'
            )
        ]

    def __str__(self):
        return f'{self.station} | {self.block_position} | {self.rate}'


class IntervalPrice(models.Model):
    """Interval - audio duration price"""

    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE, verbose_name='Радиостанция'
    )
    time_interval = models.ForeignKey(
        TimeInterval, on_delete=models.CASCADE, verbose_name='Часовой интервал'
    )
    audio_duration = models.ForeignKey(
        AudioDuration, on_delete=models.CASCADE,
        verbose_name='Хронометраж ролика'
    )
    interval_price = models.IntegerField(
        'Цена, руб.',
        validators=[
            MinValueValidator(settings.MIN_PRICE),
            MaxValueValidator(settings.MAX_PRICE)
        ]
    )

    class Meta:
        verbose_name = 'Цена часового интервала'
        verbose_name_plural = 'Цены часовых интервалов'
        constraints = [
            models.UniqueConstraint(
                fields=['station', 'time_interval', 'audio_duration'],
                name='%(class)s_unique'
            )
        ]

    def __str__(self):
        return (
            f'{self.station} | {self.time_interval} | {self.audio_duration} | '
            f'{self.interval_price}'
        )
