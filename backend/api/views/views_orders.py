from datetime import datetime

from django.db import transaction
from django.db.models import Sum
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from api.permissions import AllowAnyPost
from api.serializers.serializers_orders import (OrderCreateSerializer,
                                                CustomerSelectionSerializer)
from customers.models import Customer
from discounts.models import AmountDiscount, DaysDiscount, VolumeDiscount
from orders.models import Order, OrderCustomerSelection
from rates.models import (BlockPositionRate, MonthRate, IntervalPrice)
from settings.models import WeekDay


def get_day_name(month, day):

    date_obj = datetime(datetime.now().year, month, day)
    day_name = date_obj.strftime('%A')
    day_name_map = {
        'Monday': 'ПН',
        'Tuesday': 'ВТ',
        'Wednesday': 'СР',
        'Thursday': 'ЧТ',
        'Friday': 'ПТ',
        'Saturday': 'СБ',
        'Sunday': 'ВС'
    }
    return day_name_map.get(day_name, '')


def get_discount_value(queryset, attribute_name):
    """
    Helper function to retrieve a discount value from a queryset
    and handle None case.
    """

    discount_obj = queryset.first()
    return getattr(discount_obj, attribute_name) if discount_obj else 0


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

        block_position_rate = BlockPositionRate.objects.get(
            station__id=station.id, block_position__id=block_position.id
        ).rate

        # block_position_rate = get_discount_value(
        #     station.blockpositionrate_set.filter(
        #         block_position=block_position.id),
        #     'block_position_rate'
        # )

        month_rate = MonthRate.objects.get(
            station__id=station.id, month__id=month.id
        ).rate

        order = Order.objects.create(
            customer=customer,
            city=validated_data.pop('city'),
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

        order_customer_selections = []
        for item in customer_selection_data:
            date = item['date']
            time_interval = item['time_interval']
            audio_duration = item['audio_duration']
            week_day = get_day_name(month.id, date)

            interval_price = IntervalPrice.objects.get(
                station=station,
                time_interval=time_interval,
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
        total_days = len(order_customer_selections.distinct())
        order_volume = len(order_customer_selections)

        order.order_amount = order_amount
        order.total_days = total_days
        order.order_volume = order_volume

        # order_amount_discount = get_discount_value(
        #     station.amountdiscount_set.filter(order_amount__lte=order_amount),
        #     'order_amount_discount')
        order_amount_discount = get_discount_value(
            AmountDiscount.objects.filter(
                station=station, order_amount__lte=order_amount
            ), 'discount'
        )

        # order_days_discount= get_discount_value(
        #     station.daysdiscount_set.filter(total_days__lte=total_days),
        #     'order_days_discount')

        order_days_discount = get_discount_value(
            DaysDiscount.objects.filter(
                station=station, total_days__lte=total_days
            ), 'discount'
        )

        # order_volume_discount = get_discount_value(
        #     station.volumediscount_set.filter(order_volume__lte=order_volume),
        #     'order_volume_discount')

        order_volume_discount = get_discount_value(
            VolumeDiscount.objects.filter(
                station=station, order_volume__lte=order_volume
            ), 'discount'
        )

        order.order_amount_discount = order_amount_discount
        order.order_days_discount = order_days_discount
        order.order_volume_discount = order_volume_discount

        final_order_amount = (
                order_amount
                * block_position_rate
                * month_rate
                * other_person_rate
                * hour_selected_rate
                * (1 - order_amount_discount / 100.0)
                * (1 - order_days_discount / 100.0)
                * (1 - order_volume_discount / 100.0)
        )

        order.final_order_amount = final_order_amount
        order.save()

        return Response(status=status.HTTP_201_CREATED)
