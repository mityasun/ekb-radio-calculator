from functools import partial

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utils.abstract_models import DefaultOneMixin
from utils.validators import (validate_text, validate_email, validate_phone,
                              validate_excel_file)


class SystemText(models.Model):
    """System texts model."""

    title = models.CharField(
        'Заголовок', max_length=settings.NAME,
        validators=[partial(validate_text, max_length=settings.NAME)]
    )
    disclaimer = models.TextField(
        'Дисклеймер', max_length=settings.BIG_TEXT,
        validators=[partial(validate_text, max_length=settings.BIG_TEXT)]
    )
    phone = models.CharField(
        'Телефон', max_length=settings.PHONE, validators=[validate_phone]
    )
    email = models.EmailField(
        'Email', max_length=settings.EMAIL, validators=[validate_email]
    )
    address = models.CharField(
        'Адрес', max_length=settings.ADDRESS,
        validators=[partial(validate_text, max_length=settings.ADDRESS)]
    )
    copyright = models.CharField(
        'Копирайт', max_length=settings.COPYRIGHT,
        validators=[partial(validate_text, max_length=settings.COPYRIGHT)]
    )
    logo = models.ImageField(
        'Логотип', upload_to='system/', default=settings.DEFAULT_COMPANY_LOGO,
    )
    seo_title = models.CharField(
        'SEO Title', max_length=settings.SEO_TITLE,
        validators=[partial(validate_text, max_length=settings.SEO_TITLE)]
    )
    seo_description = models.TextField(
        'SEO description', max_length=settings.SEO_DESCRIPTION,
        validators=[
            partial(validate_text, max_length=settings.SEO_DESCRIPTION)
        ]
    )
    seo_keywords = models.CharField(
        'SEO keywords', max_length=settings.SEO_KEYWORDS,
        validators=[partial(validate_text, max_length=settings.SEO_KEYWORDS)]
    )
    privacy_text = models.TextField(
        'Политика конфиденциальности', max_length=settings.BIG_TEXT,
        validators=[partial(validate_text, max_length=settings.BIG_TEXT)]
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Системный текст'
        verbose_name_plural = 'Системные тексты'

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):

        if (
                not SystemText.objects.filter(pk=self.pk).exists()
                and SystemText.objects.exists()
        ):
            raise ValidationError(
                'There can be only one instance of this model'
            )
        super().save(*args, **kwargs)


class City(DefaultOneMixin, models.Model):
    """Cities model."""

    name = models.CharField(
        'Название города', max_length=settings.NAME, unique=True,
        validators=[partial(validate_text, max_length=settings.NAME)]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'{self.name}'


class Month(models.Model):
    """Month model."""

    JANUARY = 'Январь'
    FEBRUARY = 'Февраль'
    MARCH = 'Март'
    APRIL = 'Апрель'
    MAY = 'Май'
    JUNE = 'Июнь'
    JULY = 'Июль'
    AUGUST = 'Август'
    SEPTEMBER = 'Сентябрь'
    OCTOBER = 'Октябрь'
    NOVEMBER = 'Ноябрь'
    DECEMBER = 'Декабрь'

    MONTH_LIST = [
        (JANUARY, 'Январь'),
        (FEBRUARY, 'Февраль'),
        (MARCH, 'Март'),
        (APRIL, 'Апрель'),
        (MAY, 'Май'),
        (JUNE, 'Июнь'),
        (JULY, 'Июль'),
        (AUGUST, 'Август'),
        (SEPTEMBER, 'Сентябрь'),
        (OCTOBER, 'Октябрь'),
        (NOVEMBER, 'Ноябрь'),
        (DECEMBER, 'Декабрь'),
    ]

    month = models.CharField(
        'Название месяца', choices=MONTH_LIST, unique=True,
        max_length=max([len(month) for month, name in MONTH_LIST]),
        default=JANUARY
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Месяц'
        verbose_name_plural = 'Месяцы'

    def __str__(self):
        return f'{self.month}'


class WeekDay(models.Model):
    """Week day model."""

    MONDAY = 'ПН'
    TUESDAY = 'ВТ'
    WEDNESDAY = 'СР'
    THURSDAY = 'ЧТ'
    FRIDAY = 'ПТ'
    SATURDAY = 'СБ'
    SUNDAY = 'ВС'

    WEEK_DAY_LIST = [
        (MONDAY, 'ПН'),
        (TUESDAY, 'ВТ'),
        (WEDNESDAY, 'СР'),
        (THURSDAY, 'ЧТ'),
        (FRIDAY, 'ПТ'),
        (SATURDAY, 'СБ'),
        (SUNDAY, 'ВС'),
    ]

    week_day = models.CharField(
        'Название дня недели', choices=WEEK_DAY_LIST, unique=True,
        max_length=max([len(month) for month, name in WEEK_DAY_LIST]),
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'

    def __str__(self):
        return f'{self.week_day}'


class AudioDuration(DefaultOneMixin, models.Model):
    """Audio duration model."""

    audio_duration = models.IntegerField(
        'Хронометраж ролика, сек', unique=True,
        validators=[
            MinValueValidator(settings.MIN_AUDIO_DURATION),
            MaxValueValidator(settings.MAX_AUDIO_DURATION)
        ]
    )

    class Meta:
        ordering = ('audio_duration',)
        verbose_name = 'Хронометраж ролика'
        verbose_name_plural = 'Хронометраж роликов'

    def __str__(self):
        return f'{self.audio_duration}'


class TimeInterval(models.Model):
    """Time interval model."""

    time_interval = models.CharField(
        'Часовой интервал', max_length=settings.NAME, unique=True,
        validators=[partial(validate_text, max_length=settings.NAME)]
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Часовой интервал'
        verbose_name_plural = 'Часовые интервалы'

    def __str__(self):
        return f'{self.time_interval}'


class AudienceSex(models.Model):
    """Audience sex model."""

    MALE = 'Мужчины'
    FEMAIL = 'Женщины'
    SEX_LIST = (
        (MALE, 'Мужчины'),
        (FEMAIL, 'Женщины'),
    )

    sex = models.CharField(
        'Пол аудитории', choices=SEX_LIST, default=MALE, unique=True,
        max_length=max([len(sex) for sex, name in SEX_LIST])
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пол аудитории'
        verbose_name_plural = 'Пол аудитории'

    def __str__(self):
        return f'{self.sex}'


class AudienceAge(models.Model):
    """Audience age model."""

    age = models.CharField(
        'Возраст аудитории', max_length=settings.NAME, unique=True,
        validators=[partial(validate_text, max_length=settings.NAME)]
    )

    class Meta:
        ordering = ('age',)
        verbose_name = 'Возраст аудитории'
        verbose_name_plural = 'Возраст аудитории'

    def __str__(self):
        return f'{self.age}'


class ExcelImport(models.Model):
    """Excel import model."""

    created_at = models.DateTimeField(
        'Дата и время', auto_now=True
    )
    excel_file = models.FileField(
        'excel файл', upload_to='import/', validators=[validate_excel_file]
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Импорт данных'
        verbose_name_plural = 'Импорт данных'

    def __str__(self):
        return f'{self.created_at.strftime("%d.%m.%Y %H:%M")}'

    def save(self, *args, **kwargs):

        if (
                not ExcelImport.objects.filter(pk=self.pk).exists()
                and ExcelImport.objects.exists()
        ):
            raise ValidationError(
                'There can be only one instance of this model'
            )
        if self.pk:
            old_instance = ExcelImport.objects.get(pk=self.pk)
            default_storage.delete(old_instance.excel_file.name)
            self.excel_file.name = 'import.xlsx'
        else:
            self.excel_file.name = 'import.xlsx'
        super().save(*args, **kwargs)
