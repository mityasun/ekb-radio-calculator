from functools import partial

from django.conf import settings
from django.db import models

from utils.validators import (validate_text, validate_phone,
                              validate_email, validate_user_first_or_last_name)


class Customer(models.Model):
    """Customer model."""

    company_name = models.CharField(
        'Название организации', max_length=settings.NAME,
        validators=[partial(validate_text, max_length=settings.NAME)],
        null=True, blank=True
    )
    name = models.CharField(
        'Имя', max_length=settings.FIRST_NAME,
        validators=[validate_user_first_or_last_name]
    )
    phone = models.CharField(
        'Телефон', max_length=settings.PHONE, validators=[validate_phone]
    )
    email = models.EmailField(
        'Email', max_length=settings.EMAIL, validators=[validate_email],
        null=True, blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f'{self.name} | {self.phone}'
