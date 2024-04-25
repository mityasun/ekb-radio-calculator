from rest_framework import serializers

from rates.models import MonthRate, BlockPositionRate, IntervalPrice


class MonthRateSerializer(serializers.ModelSerializer):
    """Serializer of month rates"""

    month = serializers.ReadOnlyField(source='month.month')

    class Meta:
        model = MonthRate
        fields = ('id', 'month', 'rate')


class BlockPositionRateSerializer(serializers.ModelSerializer):
    """Serializer of block position rates"""

    block_position = serializers.ReadOnlyField(
        source='block_position.block_position'
    )

    class Meta:
        model = BlockPositionRate
        fields = ('id', 'block_position', 'rate')


class IntervalPriceSerializer(serializers.ModelSerializer):
    """Serializer of interval prices"""

    time_interval = serializers.ReadOnlyField(
        source='time_interval.time_interval'
    )
    audio_duration = serializers.ReadOnlyField(
        source='audio_duration.audio_duration'
    )

    class Meta:
        model = IntervalPrice
        fields = ('id', 'time_interval', 'audio_duration', 'interval_price')
