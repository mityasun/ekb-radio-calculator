# Generated by Django 5.0.4 on 2024-05-18 13:32

import django.core.validators
import functools
import utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudienceAge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(max_length=100, unique=True, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 100})], verbose_name='Возраст аудитории')),
            ],
            options={
                'verbose_name': 'Возраст аудитории',
                'verbose_name_plural': 'Возраст аудитории',
                'ordering': ('age',),
            },
        ),
        migrations.CreateModel(
            name='AudienceSex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('Мужчины', 'Мужчины'), ('Женщины', 'Женщины')], default='Мужчины', max_length=7, unique=True, verbose_name='Пол аудитории')),
            ],
            options={
                'verbose_name': 'Пол аудитории',
                'verbose_name_plural': 'Пол аудитории',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='AudioDuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default', models.BooleanField(default=False, verbose_name='По умолчанию')),
                ('audio_duration', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Хронометраж ролика, сек')),
            ],
            options={
                'verbose_name': 'Хронометраж ролика',
                'verbose_name_plural': 'Хронометраж роликов',
                'ordering': ('audio_duration',),
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default', models.BooleanField(default=False, verbose_name='По умолчанию')),
                ('name', models.CharField(max_length=100, unique=True, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 100})], verbose_name='Название города')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ExcelImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время')),
                ('excel_file', models.FileField(upload_to='import/', validators=[utils.validators.validate_excel_file], verbose_name='excel файл')),
            ],
            options={
                'verbose_name': 'Импорт данных',
                'verbose_name_plural': 'Импорт данных',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], default='Январь', max_length=8, unique=True, verbose_name='Название месяца')),
            ],
            options={
                'verbose_name': 'Месяц',
                'verbose_name_plural': 'Месяцы',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='SystemText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 100})], verbose_name='Заголовок')),
                ('disclaimer', models.TextField(max_length=20000, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 20000})], verbose_name='Дисклеймер')),
                ('phone', models.CharField(max_length=18, validators=[utils.validators.validate_phone], verbose_name='Телефон')),
                ('email', models.EmailField(max_length=100, validators=[utils.validators.validate_email], verbose_name='Email')),
                ('address', models.CharField(max_length=200, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 200})], verbose_name='Адрес')),
                ('copyright', models.CharField(max_length=200, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 200})], verbose_name='Копирайт')),
                ('logo', models.ImageField(default='default_images/default-company.png', upload_to='system/', verbose_name='Логотип')),
                ('seo_title', models.CharField(max_length=150, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 150})], verbose_name='SEO Title')),
                ('seo_description', models.TextField(max_length=300, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 300})], verbose_name='SEO description')),
                ('seo_keywords', models.CharField(max_length=200, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 200})], verbose_name='SEO keywords')),
                ('privacy_text', models.TextField(max_length=20000, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 20000})], verbose_name='Политика конфиденциальности')),
            ],
            options={
                'verbose_name': 'Системный текст',
                'verbose_name_plural': 'Системные тексты',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='TimeInterval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_interval', models.CharField(max_length=100, unique=True, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 100})], verbose_name='Часовой интервал')),
            ],
            options={
                'verbose_name': 'Часовой интервал',
                'verbose_name_plural': 'Часовые интервалы',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='WeekDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.CharField(choices=[('ПН', 'ПН'), ('ВТ', 'ВТ'), ('СР', 'СР'), ('ЧТ', 'ЧТ'), ('ПТ', 'ПТ'), ('СБ', 'СБ'), ('ВС', 'ВС')], max_length=2, unique=True, verbose_name='Название дня недели')),
            ],
            options={
                'verbose_name': 'День недели',
                'verbose_name_plural': 'Дни недели',
                'ordering': ('id',),
            },
        ),
    ]
