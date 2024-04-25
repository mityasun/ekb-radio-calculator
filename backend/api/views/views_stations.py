from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, cache_control
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response

from api.mixins import ReadOnlyViewSet
from api.serializers.serializers_stations import (StationsSerializer,
                                                  StationsShortSerializer)
from stations.models import RadioStation
from utils.utils import generate_redis_key


class StationViewSet(ReadOnlyViewSet):
    """ViewSet for radio stations"""

    serializer_class = StationsSerializer
    queryset = RadioStation.objects.select_related('city').prefetch_related(
        'audiencesexstation_set__sex', 'audienceagestation_set__age',
        'monthrate_set__month', 'blockpositionrate_set__block_position',
        'intervalprice_set__time_interval',
        'intervalprice_set__audio_duration'
    )
    http_method_names = ['get']

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_control(no_cache=True, must_revalidate=True))
    def dispatch(self, *args, **kwargs):
        return cache_page(
            settings.CACHE_TTL,
            key_prefix=generate_redis_key(self, 'radiostations')
        )(super(StationViewSet, self).dispatch)(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        """List of radio stations"""

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = StationsShortSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve one radio station"""

        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
