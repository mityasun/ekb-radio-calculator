from rest_framework import serializers

from api.serializers.serializers_settings import (TimeIntervalSerializer,
                                                  AudioDurationSerializer,
                                                  BlockPositionSerializer)
from rates.models import MonthRate, BlockPositionRate, IntervalPrice


class MonthRateSerializer(serializers.ModelSerializer):
    """Serializer of month rates"""

    id = serializers.ReadOnlyField(source='month.id')

    class Meta:
        model = MonthRate
        fields = ('id', 'rate')


class BlockPositionRateSerializer(serializers.ModelSerializer):
    """Serializer of block position rates"""

    block_position = BlockPositionSerializer(read_only=True)

    class Meta:
        model = BlockPositionRate
        fields = ('block_position', 'rate')


class IntervalPriceSerializer(serializers.ModelSerializer):
    """Serializer of interval prices"""

    time_interval = TimeIntervalSerializer(read_only=True)
    audio_duration = AudioDurationSerializer(read_only=True)

    class Meta:
        model = IntervalPrice
        fields = ('time_interval', 'audio_duration', 'interval_price')
