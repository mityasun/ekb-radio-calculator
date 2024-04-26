# Generated by Django 5.0.4 on 2024-04-24 18:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка, %')),
                ('order_amount', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000000)], verbose_name='Сумма заказа, руб.')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stations.radiostation', verbose_name='Радиостанция')),
            ],
            options={
                'verbose_name': 'Скидка за сумму заказа, %',
                'verbose_name_plural': 'Скидки за сумму заказа, %',
            },
        ),
        migrations.CreateModel(
            name='DaysDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка, %')),
                ('total_days', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)], verbose_name='Количество дней')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stations.radiostation', verbose_name='Радиостанция')),
            ],
            options={
                'verbose_name': 'Скидка за продолжительность РК, %',
                'verbose_name_plural': 'Скидки за продолжительность РК, %',
            },
        ),
        migrations.CreateModel(
            name='VolumeDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка, %')),
                ('order_volume', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(496)], verbose_name='Количество выходов')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stations.radiostation', verbose_name='Радиостанция')),
            ],
            options={
                'verbose_name': 'Скидка за кол-во выходов в сетке, %',
                'verbose_name_plural': 'Скидки за кол-во выходов в сетке, %',
            },
        ),
        migrations.AddConstraint(
            model_name='amountdiscount',
            constraint=models.UniqueConstraint(fields=('order_amount', 'station'), name='amountdiscount_unique'),
        ),
        migrations.AddConstraint(
            model_name='daysdiscount',
            constraint=models.UniqueConstraint(fields=('total_days', 'station'), name='daysdiscount_unique'),
        ),
        migrations.AddConstraint(
            model_name='volumediscount',
            constraint=models.UniqueConstraint(fields=('order_volume', 'station'), name='volumediscount_unique'),
        ),
    ]