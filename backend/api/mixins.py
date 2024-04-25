from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import (CustomPageNumberPagination,
                         CaseInsensitiveOrderingFilter)
from api.permissions import IsAdminAuthorOrReadOnly


class ReadOnlyViewSet(ReadOnlyModelViewSet):
    """Main viewset for read only models"""

    permission_classes = [IsAdminAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend, CaseInsensitiveOrderingFilter)
    ordering = ('id',)
    ordering_fields = ('id',)
    lookup_field = 'id'
