from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, cache_control
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from django_ratelimit.decorators import ratelimit

from api.filters import NameFilter, CaseInsensitiveOrderingFilter
from api.mixins import ReadOnlyViewSet
from api.serializers.serializers_settings import (SystemTextSerializer,
                                                  CitySerializer,
                                                  AudioDurationSerializer,
                                                  BlockPositionSerializer,
                                                  TimeIntervalSerializer)
from rates.models import BlockPosition
from settings.models import City, AudioDuration, TimeInterval, SystemText
from utils.utils import generate_redis_key


class SystemTextViewSet(ReadOnlyViewSet):
    """ViewSet for system texts"""

    serializer_class = SystemTextSerializer
    queryset = SystemText.objects.all()

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_control(no_cache=True, must_revalidate=True))
    @method_decorator(ratelimit(key='ip', rate='1/s', block=True))
    def dispatch(self, *args, **kwargs):
        return cache_page(
            settings.CACHE_TTL,
            key_prefix=generate_redis_key(self, 'system-texts')
        )(super(SystemTextViewSet, self).dispatch)(*args, **kwargs)


class CityViewSet(ReadOnlyViewSet):
    """ViewSet for cities"""

    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (
        NameFilter, DjangoFilterBackend, CaseInsensitiveOrderingFilter
    )
    search_fields = ('@name',)
    ordering_fields = ('id', 'name')

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_control(no_cache=True, must_revalidate=True))
    @method_decorator(ratelimit(key='ip', rate='1/s', block=True))
    def dispatch(self, *args, **kwargs):
        return cache_page(
            settings.CACHE_TTL,
            key_prefix=generate_redis_key(self, 'cities')
        )(super(CityViewSet, self).dispatch)(*args, **kwargs)


class AudioDurationViewSet(ReadOnlyViewSet):
    """ViewSet for audio durations"""

    serializer_class = AudioDurationSerializer
    queryset = AudioDuration.objects.all()

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_control(no_cache=True, must_revalidate=True))
    def dispatch(self, *args, **kwargs):
        return cache_page(
            settings.CACHE_TTL,
            key_prefix=generate_redis_key(self, 'audio-durations')
        )(super(AudioDurationViewSet, self).dispatch)(*args, **kwargs)


class BlockPositionViewSet(ReadOnlyViewSet):
    """ViewSet for block positions"""

    serializer_class = BlockPositionSerializer
    queryset = BlockPosition.objects.all()

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_control(no_cache=True, must_revalidate=True))
    def dispatch(self, *args, **kwargs):
        return cache_page(
            settings.CACHE_TTL,
            key_prefix=generate_redis_key(self, 'block-positions')
        )(super(BlockPositionViewSet, self).dispatch)(*args, **kwargs)


class TimeIntervalViewSet(ReadOnlyViewSet):
    """ViewSet for time intervals"""

    serializer_class = TimeIntervalSerializer
    queryset = TimeInterval.objects.all()

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_control(no_cache=True, must_revalidate=True))
    def dispatch(self, *args, **kwargs):
        return cache_page(
            settings.CACHE_TTL,
            key_prefix=generate_redis_key(self, 'time-intervals')
        )(super(TimeIntervalViewSet, self).dispatch)(*args, **kwargs)
