from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from rest_framework import serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination

from utils.validators import validate_search_query


class CustomPageNumberPagination(PageNumberPagination):
    """Custom pagination and validation for limit and page params"""

    page_size_query_param = 'limit'

    def get_page_size(self, request):
        """Validation for limit param."""

        limit = request.query_params.get(self.page_size_query_param)
        if limit is not None:
            try:
                limit = int(limit)
            except (TypeError, ValueError):
                raise serializers.ValidationError(
                    {'limit': 'может быть только целым числом'}
                )
            if limit < 1 or limit > settings.MAX_LIMIT:
                raise serializers.ValidationError(
                    {'limit': 'min 1, max 100'}
                )
        return super().get_page_size(request)

    def get_page_number(self, request, paginator):
        """Validation for page param."""

        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number is not None:
            try:
                page_number = int(page_number)
            except (TypeError, ValueError):
                raise serializers.ValidationError(
                    {'page': 'может быть только целым числом'}
                )
            if page_number < 1:
                raise serializers.ValidationError(
                    {'page': 'может быть только положительным числом'}
                )
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number


class NameFilter(SearchFilter):
    """Search by name and validations query"""

    search_param = 'name'

    def get_search_fields(self, view, request):
        name_param = request.query_params.get('name')
        if name_param is not None:
            try:
                validate_search_query(name_param)
            except ValidationError as error:
                raise serializers.ValidationError(error)
            return ['name']
        return super().get_search_fields(view, request)


class CaseInsensitiveOrderingFilter(OrderingFilter):
    """Ordering with case-insensitive by name field and allowed params"""

    def get_ordering(self, request, queryset, view):
        """Allowed only specific params to be passed to the ordering"""

        allowed_list = ['name', '-name', 'id', '-id']

        params = request.query_params.get(self.ordering_param)

        if params is not None:
            if params == "" or params.isspace():
                raise serializers.ValidationError(
                    {'ordering': 'пустой параметр.'}
                )
            if params not in allowed_list:
                raise serializers.ValidationError(
                    {'ordering': 'передан некорректный параметр.'}
                )
            fields = [param.strip() for param in params.split(',')]
            ordering = self.remove_invalid_fields(
                queryset, fields, view, request
            )
            if ordering:
                return ordering
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        """Ordering filter with case-insensitive by name field"""

        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            new_ordering = []
            for field in ordering:
                if field == 'name' or field == '-name':
                    if field.startswith('-'):
                        new_ordering.append(Lower(field[1:]).desc())
                    else:
                        new_ordering.append(Lower(field).asc())
                else:
                    new_ordering.append(field)
            return queryset.order_by(*new_ordering)
        return queryset
