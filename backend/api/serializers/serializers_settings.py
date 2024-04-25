from rest_framework import serializers

from rates.models import BlockPosition
from settings.models import City, AudioDuration, TimeInterval, SystemText
from stations.models import AudienceSexStation, AudienceAgeStation


class SystemTextSerializer(serializers.ModelSerializer):
    """Serializer of system texts"""

    class Meta:
        model = SystemText
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    """Serializer of cities"""

    class Meta:
        model = City
        fields = '__all__'


class BlockPositionSerializer(serializers.ModelSerializer):
    """Serializer of block positions"""

    class Meta:
        model = BlockPosition
        fields = '__all__'


class AudioDurationSerializer(serializers.ModelSerializer):
    """Serializer of audio durations"""

    class Meta:
        model = AudioDuration
        fields = '__all__'


class TimeIntervalSerializer(serializers.ModelSerializer):
    """Serializer of time intervals"""

    class Meta:
        model = TimeInterval
        fields = '__all__'


class AudienceSexStationSerializer(serializers.ModelSerializer):
    """Serializer of audience sex"""

    sex = serializers.ReadOnlyField(source='sex.sex')

    class Meta:
        model = AudienceSexStation
        fields = ('id', 'sex', 'percent')


class AudienceAgeStationSerializer(serializers.ModelSerializer):
    """Serializer of audience age"""

    age = serializers.ReadOnlyField(source='age.age')

    class Meta:
        model = AudienceAgeStation
        fields = ('id', 'age', 'percent')
