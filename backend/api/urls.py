from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.views_orders import OrderViewSet
from api.views.views_settings import (SystemTextViewSet, CityViewSet,
                                      AudioDurationViewSet,
                                      BlockPositionViewSet,
                                      TimeIntervalViewSet)
from api.views.views_stations import StationViewSet

router_v1 = DefaultRouter()
router_v1.register(r'system-texts', SystemTextViewSet, basename='system-texts')
router_v1.register(r'stations', StationViewSet, basename='stations')
router_v1.register(r'cities', CityViewSet, basename='cities')
router_v1.register(
    r'audio_durations', AudioDurationViewSet, basename='audio_durations'
)
router_v1.register(
    r'block_positions', BlockPositionViewSet, basename='block_positions'
)
router_v1.register(
    r'time_intervals', TimeIntervalViewSet, basename='time_intervals'
)
router_v1.register(
    r'order', OrderViewSet, basename='order'
)


urlpatterns = [
    path('', include(router_v1.urls)),
]
