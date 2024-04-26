import asyncio

from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from api.permissions import AllowAnyPost
from api.serializers.serializers_orders import (OrderCreateSerializer,
                                                CustomerSelectionSerializer,
                                                OrderPdfSerializer)
from api.utils import (get_day_name, get_discount_value, create_pdf,
                       send_pdf_to_group)
from customers.models import Customer
from discounts.models import AmountDiscount, DaysDiscount, VolumeDiscount
from orders.models import Order, OrderCustomerSelection
from rates.models import BlockPositionRate, MonthRate, IntervalPrice
from settings.models import WeekDay


class OrderPdfViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """ViewSet for Order"""

    queryset = Order.objects.prefetch_related(
        'customer', 'city', 'station', 'block_position', 'month', 'station'
    )
    http_method_names = ['post']
    serializer_class = OrderPdfSerializer
    permission_classes = [AllowAnyPost]

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        city = validated_data.pop('city')
        station = validated_data.pop('station')
        block_position = validated_data.pop('block_position')
        month = validated_data.pop('month')

        other_person_rate = (
            station.other_person_rate
            if validated_data.pop('other_person_rate')
            else 1
        )

        hour_selected_rate = (
            station.hour_selected_rate
            if validated_data.pop('hour_selected_rate')
            else 1
        )

        block_position_rate = get_object_or_404(
            BlockPositionRate,
            station__id=station.id, block_position__id=block_position.id
        ).rate

        month_rate = get_object_or_404(
            MonthRate,
            station__id=station.id, month__id=month.id
        ).rate

        customer_selection_data = validated_data.pop('customer_selection')
        customer_selection_serializer = CustomerSelectionSerializer(
            data=customer_selection_data, many=True
        )
        customer_selection_serializer.is_valid(raise_exception=True)

        unique_dates = set()
        order_amount = 0
        total_days = 0
        order_volume = 0

        for item in customer_selection_data:
            date = item['date']
            time_interval = item['time_interval']
            audio_duration = item['audio_duration']
            interval_price = get_object_or_404(
                IntervalPrice, station=station, time_interval=time_interval,
                audio_duration=audio_duration
            ).interval_price
            order_amount += interval_price
            if date not in unique_dates:
                total_days += 1
                unique_dates.add(date)
            order_volume += 1

        order_amount_with_rates = (
                order_amount
                * block_position_rate
                * month_rate
                * other_person_rate
                * hour_selected_rate
        )

        order_amount_discount = get_discount_value(
            AmountDiscount.objects.filter(
                station=station, order_amount__lte=order_amount_with_rates
            ), '-order_amount', 'discount'
        )

        order_days_discount = get_discount_value(
            DaysDiscount.objects.filter(
                station=station, total_days__lte=total_days
            ), '-total_days', 'discount'
        )

        order_volume_discount = get_discount_value(
            VolumeDiscount.objects.filter(
                station=station, order_volume__lte=order_volume
            ), '-order_volume', 'discount'
        )

        final_order_amount = (
                order_amount_with_rates
                * (1 - order_amount_discount / 100.0)
                * (1 - order_days_discount / 100.0)
                * (1 - order_volume_discount / 100.0)
        )

        pdf = create_pdf(
            city, station, month, block_position, block_position_rate,
            month_rate, other_person_rate, hour_selected_rate,
            order_amount_with_rates, order_amount_discount, total_days,
            order_days_discount, order_volume, order_volume_discount,
            final_order_amount, customer_selection_data, False
        )
        return pdf


class OrderViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """ViewSet for Order"""

    queryset = Order.objects.prefetch_related(
        'customer', 'city', 'station', 'block_position', 'month', 'station'
    )
    http_method_names = ['post']
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAnyPost]

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        customer_data = validated_data.pop('customer')
        customer = Customer.objects.create(**customer_data)

        city = validated_data.pop('city')
        station = validated_data.pop('station')
        block_position = validated_data.pop('block_position')
        month = validated_data.pop('month')

        other_person_rate = (
            station.other_person_rate
            if validated_data.pop('other_person_rate')
            else 1
        )

        hour_selected_rate = (
            station.hour_selected_rate
            if validated_data.pop('hour_selected_rate')
            else 1
        )

        block_position_rate = get_object_or_404(
            BlockPositionRate,
            station__id=station.id, block_position__id=block_position.id
        ).rate

        month_rate = get_object_or_404(
            MonthRate,
            station__id=station.id, month__id=month.id
        ).rate

        order = Order.objects.create(
            customer=customer,
            city=city,
            station=station,
            block_position=block_position,
            block_position_rate=block_position_rate,
            month=month,
            month_rate=month_rate,
            other_person_rate=other_person_rate,
            hour_selected_rate=hour_selected_rate,
            order_amount=0,
            total_days=0,
            order_volume=0,
            final_order_amount=0
        )

        customer_selection_data = validated_data.pop('customer_selection')
        customer_selection_serializer = CustomerSelectionSerializer(
            data=customer_selection_data, many=True
        )
        customer_selection_serializer.is_valid(raise_exception=True)

        unique_dates = set()
        total_days = 0
        order_customer_selections = []
        for item in customer_selection_data:
            date = item['date']
            time_interval = item['time_interval']
            audio_duration = item['audio_duration']
            week_day = get_day_name(month.id, date)
            if date not in unique_dates:
                total_days += 1
                unique_dates.add(date)
            interval_price = get_object_or_404(
                IntervalPrice, station=station, time_interval=time_interval,
                audio_duration=audio_duration
            ).interval_price
            order_customer_selections.append(
                OrderCustomerSelection(
                    order=order,
                    date=date,
                    week_day=WeekDay.objects.get(week_day=week_day),
                    time_interval_id=time_interval,
                    audio_duration_id=audio_duration,
                    interval_price=interval_price
                )
            )
        OrderCustomerSelection.objects.bulk_create(order_customer_selections)

        order_customer_selections = OrderCustomerSelection.objects.filter(
            order=order
        )
        order_amount = order_customer_selections.aggregate(
            total_interval_price=Sum('interval_price')
        )['total_interval_price'] or 0
        order_volume = len(order_customer_selections)

        order.order_amount = order_amount
        order.total_days = total_days
        order.order_volume = order_volume

        order_amount_with_rates = (
                order_amount
                * block_position_rate
                * month_rate
                * other_person_rate
                * hour_selected_rate
        )

        order_amount_discount = get_discount_value(
            AmountDiscount.objects.filter(
                station=station, order_amount__lte=order_amount_with_rates
            ), '-order_amount', 'discount'
        )

        order_days_discount = get_discount_value(
            DaysDiscount.objects.filter(
                station=station, total_days__lte=total_days
            ), '-total_days', 'discount'
        )

        order_volume_discount = get_discount_value(
            VolumeDiscount.objects.filter(
                station=station, order_volume__lte=order_volume
            ), '-order_volume', 'discount'
        )

        order.order_amount_discount = order_amount_discount
        order.order_days_discount = order_days_discount
        order.order_volume_discount = order_volume_discount

        final_order_amount = (
                order_amount_with_rates
                * (1 - order_amount_discount / 100.0)
                * (1 - order_days_discount / 100.0)
                * (1 - order_volume_discount / 100.0)
        )

        order.final_order_amount = final_order_amount
        order.save()

        pdf_file_path = create_pdf(
            city, station, month, block_position, block_position_rate,
            month_rate, other_person_rate, hour_selected_rate,
            order_amount_with_rates, order_amount_discount, total_days,
            order_days_discount, order_volume, order_volume_discount,
            final_order_amount, customer_selection_data, True
        )
        order_info = (f'Заказ:\n'
                      f'Название компании: {customer.company_name}\n'
                      f'Имя: {customer.name}\n'
                      f'Телефон: {customer.phone}\n'
                      f'email: {customer.email}')
        # asyncio.run(send_pdf_to_group(order_info, pdf_file_path))

        return Response(status=status.HTTP_201_CREATED)
