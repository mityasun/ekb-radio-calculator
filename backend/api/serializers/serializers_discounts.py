from rest_framework import serializers

from discounts.models import AmountDiscount, DaysDiscount, VolumeDiscount


class AmountDiscountSerializer(serializers.ModelSerializer):
    """Serializer of amount discounts"""

    class Meta:
        model = AmountDiscount
        fields = ('order_amount', 'discount')


class DaysDiscountSerializer(serializers.ModelSerializer):
    """Serializer of days discounts"""

    class Meta:
        model = DaysDiscount
        fields = ('total_days', 'discount')


class VolumeDiscountSerializer(serializers.ModelSerializer):
    """Serializer of volume discounts"""

    class Meta:
        model = VolumeDiscount
        fields = ('order_volume', 'discount')
