from functools import partial

from django.conf import settings
from rest_framework import serializers

from customers.models import Customer
from utils.validators import (validate_text, validate_phone, validate_email,
                              validate_user_first_or_last_name)


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer of customers"""

    company_name = serializers.CharField(
        required=False, max_length=settings.NAME,
        validators=[partial(validate_text, max_length=settings.NAME)]
    )
    name = serializers.CharField(
        required=True, max_length=settings.FIRST_NAME,
        validators=[validate_user_first_or_last_name]
    )
    phone = serializers.CharField(
        required=True, max_length=settings.PHONE, validators=[validate_phone]
    )
    email = serializers.EmailField(
        required=False, max_length=settings.EMAIL, validators=[validate_email]
    )

    class Meta:
        model = Customer
        fields = '__all__'
