from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from utils.validators import (validate_email, validate_user_first_or_last_name,
                              validate_username, validate_password)


class User(AbstractUser):
    """User model"""

    email = models.EmailField(
        'Email', max_length=settings.EMAIL, unique=True,
        validators=[validate_email]
    )
    username = models.CharField(
        'Никнэйм', max_length=settings.USERNAME, unique=True,
        validators=[validate_username]
    )
    first_name = models.CharField(
        'Имя', null=True, blank=True, max_length=settings.FIRST_NAME,
        validators=[validate_user_first_or_last_name]
    )
    last_name = models.CharField(
        'Фамилия', null=True, blank=True, max_length=settings.LAST_NAME,
        validators=[validate_user_first_or_last_name]
    )
    password = models.CharField(
        'Пароль', max_length=settings.PASSWORD,
        validators=[validate_password]
    )
    is_active = models.BooleanField(
        'Пользователь активированный', default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    def clean(self):
        self.email = str(self.email).lower()
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError(
                {'email': 'Пользователь с таким email уже существует'})
        super().clean()
