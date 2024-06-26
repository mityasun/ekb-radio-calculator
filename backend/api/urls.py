from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.views_orders import OrderViewSet, OrderPdfViewSet
from api.views.views_settings import SystemTextViewSet, CityViewSet
from api.views.views_stations import StationViewSet

router_v1 = DefaultRouter()
router_v1.register(r'system-texts', SystemTextViewSet, basename='system-texts')
router_v1.register(r'stations', StationViewSet, basename='stations')
router_v1.register(r'cities', CityViewSet, basename='cities')
router_v1.register(
    r'order', OrderViewSet, basename='order'
)
router_v1.register(
    r'order-pdf', OrderPdfViewSet, basename='order-pdf'
)


urlpatterns = [
    path('', include(router_v1.urls)),
]
