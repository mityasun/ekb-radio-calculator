# Generated by Django 5.0.4 on 2024-04-26 18:40

import django.core.validators
import django.db.models.deletion
import functools
import utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadioStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default', models.BooleanField(default=False, verbose_name='По умолчанию')),
                ('name', models.CharField(max_length=100, unique=True, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 100})], verbose_name='Название')),
                ('title', models.CharField(max_length=100, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 100})], verbose_name='Заголовок')),
                ('description', models.TextField(max_length=5000, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 5000})], verbose_name='Описание радиостанции')),
                ('broadcast_zone', models.CharField(max_length=200, validators=[functools.partial(utils.validators.validate_text, *(), **{'max_length': 200})], verbose_name='Зона вещания')),
                ('reach_dly', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Reach Dly, чел')),
                ('reach_dly_percent', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Reach Dly, %')),
                ('other_person_rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Коэффициент за упоминание 3-х лиц')),
                ('hour_selected_rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Коэффициент за выбор часа')),
                ('logo', models.ImageField(blank=True, default='default_images/default-station.jpg', null=True, upload_to='stations/', validators=[utils.validators.validate_image], verbose_name='Лого')),
                ('city', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='station_city', to='settings.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Радиостанция',
                'verbose_name_plural': 'Радиостанции',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='AudienceSexStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Процент')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.audiencesex', verbose_name='Пол')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stations.radiostation', verbose_name='Радиостанция')),
            ],
            options={
                'verbose_name': 'Пол аудитории',
                'verbose_name_plural': 'Пол аудитории',
            },
        ),
        migrations.CreateModel(
            name='AudienceAgeStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Процент')),
                ('age', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.audienceage', verbose_name='Возраст аудитории')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stations.radiostation', verbose_name='Радиостанция')),
            ],
            options={
                'verbose_name': 'Возраст аудитории',
                'verbose_name_plural': 'Возраст аудитории',
            },
        ),
        migrations.AddConstraint(
            model_name='audiencesexstation',
            constraint=models.UniqueConstraint(fields=('sex', 'station'), name='audiencesexstation_unique'),
        ),
        migrations.AddConstraint(
            model_name='audienceagestation',
            constraint=models.UniqueConstraint(fields=('age', 'station'), name='audienceagestation_unique'),
        ),
    ]
