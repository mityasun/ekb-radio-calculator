from functools import partial
from io import BytesIO

from PIL import Image as PilImage
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from settings.models import City, AudienceAge, AudienceSex
from utils.abstract_models import DefaultOneMixin
from utils.utils import reduce_image, to_translit
from utils.validators import validate_text, validate_image


class RadioStation(DefaultOneMixin, models.Model):
    """Radio station model."""

    name = models.CharField(
        'Название', max_length=settings.NAME,
        validators=[partial(validate_text, max_length=settings.NAME)]
    )
    title = models.CharField(
        'Заголовок', max_length=settings.NAME,
        validators=[partial(validate_text, max_length=settings.NAME)]
    )
    description = models.TextField(
        'Описание радиостанции', max_length=settings.DESCRIPTION,
        validators=[partial(validate_text, max_length=settings.DESCRIPTION)]
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_DEFAULT, default=1,
        related_name='station_city', verbose_name='Город'
    )
    broadcast_zone = models.CharField(
        'Зона вещания', max_length=settings.BROADCAST_ZONE,
        validators=[partial(validate_text, max_length=settings.BROADCAST_ZONE)]
    )
    reach_dly = models.IntegerField(
        'Reach Dly, чел',
        validators=[
            MinValueValidator(settings.MIN_REACH_DLY),
            MaxValueValidator(settings.MAX_REACH_DLY)
        ]
    )
    reach_dly_percent = models.FloatField(
        'Reach Dly, %',
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
    logo = models.ImageField(
        'Лого', blank=True, null=True,
        upload_to='stations/', default=settings.DEFAULT_LOGO,
        validators=[validate_image]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Радиостанция'
        verbose_name_plural = 'Радиостанции'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):

        file_name = to_translit(self.logo.name)
        if self.pk:
            old_logo = RadioStation.objects.get(pk=self.pk).logo
            if self.logo != old_logo:
                img_bytes = BytesIO(self.logo.read())
                img = PilImage.open(img_bytes)
                default_storage.delete(old_logo.name)
                self.logo = reduce_image(
                    img, max_size=settings.IMAGE_SIZE, image_name=file_name
                )
        else:
            img_bytes = BytesIO(self.logo.read())
            img = PilImage.open(img_bytes)
            self.logo = reduce_image(
                img, max_size=settings.IMAGE_SIZE, image_name=file_name
            )
        super().save(*args, **kwargs)


class AbstractSocialStation(models.Model):
    """Abstract model for social data of station."""

    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE, verbose_name='Радиостанция'
    )
    percent = models.FloatField(
        'Процент', validators=[
            MinValueValidator(settings.MIN_PERCENT),
            MaxValueValidator(settings.MAX_PERCENT)
        ]
    )

    class Meta:
        abstract = True


class AudienceSexStation(AbstractSocialStation):
    """Radio station audience sex model"""

    sex = models.ForeignKey(
        AudienceSex, on_delete=models.CASCADE, verbose_name='Пол'
    )

    class Meta:
        verbose_name = 'Пол аудитории'
        verbose_name_plural = 'Пол аудитории'
        constraints = [
            models.UniqueConstraint(
                fields=['sex', 'station'], name='%(class)s_unique'
            )
        ]

    def __str__(self):
        return f'{self.sex}'


class AudienceAgeStation(AbstractSocialStation):
    """Radio station audience age model"""

    age = models.ForeignKey(
        AudienceAge, on_delete=models.CASCADE,
        verbose_name='Возраст аудитории', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Возраст аудитории'
        verbose_name_plural = 'Возраст аудитории'
        constraints = [
            models.UniqueConstraint(
                fields=['age', 'station'], name='%(class)s_unique'
            )
        ]

    def __str__(self):
        return f'{self.age}'
