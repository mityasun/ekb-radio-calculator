from rest_framework import serializers

from api.serializers.serializers_discounts import (AmountDiscountSerializer,
                                                   VolumeDiscountSerializer,
                                                   DaysDiscountSerializer)
from api.serializers.serializers_rates import (MonthRateSerializer,
                                               BlockPositionRateSerializer,
                                               IntervalPriceSerializer)
from api.serializers.serializers_settings import (CitySerializer,
                                                  AudienceSexStationSerializer,
                                                  AudienceAgeStationSerializer)
from stations.models import RadioStation


class StationsSerializer(serializers.ModelSerializer):
    """Serializer of radio stations"""

    default = serializers.BooleanField(read_only=True)
    name = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    city = CitySerializer(read_only=True)
    broadcast_zone = serializers.CharField(read_only=True)
    reach_dly = serializers.IntegerField(read_only=True)
    reach_dly_percent = serializers.FloatField(read_only=True)
    other_person_rate = serializers.FloatField(read_only=True)
    hour_selected_rate = serializers.FloatField(read_only=True)
    logo = serializers.ImageField(read_only=True)
    audience_sex = AudienceSexStationSerializer(
        source='audiencesexstation_set', many=True, read_only=True
    )
    audience_age = AudienceAgeStationSerializer(
        source='audienceagestation_set', many=True, read_only=True
    )
    month_rate = MonthRateSerializer(
        source='monthrate_set', many=True, read_only=True
    )
    block_position_rate = BlockPositionRateSerializer(
        source='blockpositionrate_set', many=True, read_only=True
    )
    interval_price = IntervalPriceSerializer(
        source='intervalprice_set', many=True, read_only=True
    )
    amount_discount = AmountDiscountSerializer(
        source='amountdiscount_set', many=True, read_only=True
    )
    days_discount = DaysDiscountSerializer(
        source='daysdiscount_set', many=True, read_only=True
    )
    volume_discount = VolumeDiscountSerializer(
        source='volumediscount_set', many=True, read_only=True
    )

    class Meta:
        model = RadioStation
        fields = '__all__'


class StationsShortSerializer(StationsSerializer):
    """Serializer of radio stations short"""

    class Meta(StationsSerializer.Meta):
        fields = ('id', 'default', 'name')
