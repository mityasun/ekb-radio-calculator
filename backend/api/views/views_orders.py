import asyncio
import logging
import os
from typing import Union, Tuple

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from api.permissions import AllowAnyPost
from api.serializers.serializers_orders import (OrderCreateSerializer,
                                                CustomerSelectionSerializer,
                                                OrderPdfSerializer)
from api.utils import (get_day_name, get_discount_value, create_pdf,
                       send_email_with_order, send_pdf_to_group)
from customers.models import Customer
from discounts.models import AmountDiscount, DaysDiscount, VolumeDiscount
from orders.models import Order, OrderCustomerSelection
from rates.models import (BlockPositionRate, MonthRate, IntervalPrice,
                          BlockPosition)
from settings.models import WeekDay, Month
from stations.models import RadioStation

logger = logging.getLogger(__name__)


def get_rates(
        station: RadioStation,
        block_position: BlockPosition,
        month: Month,
        validated_data: dict
) -> Tuple[float, float, float, float]:
    """
    Get the rates based on the station, block position, month
    and validated data.

    Args:
        station (RadioStation): The radio station.
        block_position (BlockPosition): The block position object.
        month (Month): The month object.
        validated_data (dict): The validated data from the serializer.

    Returns:
        Tuple[float, float, float, float]:
        A tuple containing the other person rate, hour selected rate,
        block position rate and month rate.
    """

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

    return (
        other_person_rate, hour_selected_rate, block_position_rate, month_rate
    )


def process_customer_selection(
    station: RadioStation,
    customer_selection_data,
    month: Month,
    order: Order = None
) -> Tuple[int, int, int, list]:
    """
    Process the customer selection data to calculate order amount, total days,
    and order volume. Optionally prepare a list of OrderCustomerSelection
    objects to create.

    Args:
        station (RadioStation): The station object.
        customer_selection_data: The customer selection data.
        month (Month): The month object.
        order (Order, optional): The order object if create

    Returns:
        Tuple[int, int, int, list]:
        A tuple containing the order amount, total days, order volume
        and optionally a list of OrderCustomerSelection objects.
    """

    customer_selection_serializer = CustomerSelectionSerializer(
        data=customer_selection_data, many=True
    )
    customer_selection_serializer.is_valid(raise_exception=True)

    unique_dates = set()
    order_amount = 0
    total_days = 0
    order_volume = 0
    order_customer_selections = []
    for item in customer_selection_data:
        date = item['date']
        time_interval = item['time_interval']
        audio_duration = item['audio_duration']
        week_day = get_day_name(month.id, date)
        interval_price = get_object_or_404(
            IntervalPrice, station=station,
            time_interval=time_interval,
            audio_duration=audio_duration
        ).interval_price
        order_amount += interval_price
        if date not in unique_dates:
            total_days += 1
            unique_dates.add(date)
        order_volume += 1
        if order:
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
    return order_amount, total_days, order_volume, order_customer_selections


def main_calculating(
        station: RadioStation,
        other_person_rate: float,
        hour_selected_rate: float,
        block_position_rate: float,
        month_rate: float,
        customer_selection_data: list,
        month: Month,
        order: Order = None,
) -> Tuple[int, int, list, float, float, float, int, int]:
    """
    Calculate the final order amount along with discounts applied.

    Args:
        station (RadioStation): The radio station.
        other_person_rate (float): The rate applied for other person factors.
        hour_selected_rate (float): The rate applied for hour selection.
        block_position_rate (float): The rate applied for block position.
        month_rate (float): The rate applied for month.
        customer_selection_data: Data related to customer selections.
        month (Month): The month for which the order is being calculated.
        order (Order, optional): The order object, defaults to None.

    Returns:
        Tuple[int, int, list, float, float, float, float, float]:
            - Total days: Total number of days for the order.
            - Order volume: Volume of the order.
            - Order customer selections: Customer selections for the order.
            - Order amount discount: Discount applied based on order amount.
            - Order days discount: Discount applied based on total days.
            - Order volume discount: Discount applied based on order volume.
            - Order amount with rates: Total order amount with rates applied.
            - Final order amount: Final order amount after applying discounts.
    """

    order_amount, total_days, order_volume, order_customer_selections = (
        process_customer_selection(
            station, customer_selection_data, month, order
        )
    )

    order_amount_with_rates = round(
        (
            order_amount
            * block_position_rate
            * month_rate
            * other_person_rate
            * hour_selected_rate
        )
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

    final_order_amount = round(
        (
            order_amount_with_rates
            * (1 - order_amount_discount / 100.0)
            * (1 - order_days_discount / 100.0)
            * (1 - order_volume_discount / 100.0)
        )
    )

    return (
        total_days, order_volume, order_customer_selections,
        order_amount_discount, order_days_discount,
        order_volume_discount, order_amount_with_rates, final_order_amount
    )


class OrderPdfViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """ViewSet for create pdf by order"""

    queryset = Order.objects.prefetch_related(
        'customer', 'city', 'station', 'block_position', 'month', 'station'
    )
    http_method_names = ['post']
    serializer_class = OrderPdfSerializer
    permission_classes = [AllowAnyPost]

    @method_decorator(ratelimit(key='ip', rate='12/m', block=True))
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        city = validated_data.pop('city')
        station = validated_data.pop('station')
        block_position = validated_data.pop('block_position')
        month = validated_data.pop('month')
        customer_selection_data = validated_data.pop('customer_selection')

        (
            other_person_rate, hour_selected_rate, block_position_rate,
            month_rate
        ) = get_rates(station, block_position, month, validated_data)

        (
            total_days, order_volume, order_customer_selections,
            order_amount_discount, order_days_discount,
            order_volume_discount, order_amount_with_rates, final_order_amount
        ) = main_calculating(
            station, other_person_rate, hour_selected_rate,
            block_position_rate, month_rate, customer_selection_data, month
        )

        try:
            pdf = create_pdf(
                city, station, month, block_position, block_position_rate,
                month_rate, other_person_rate, hour_selected_rate,
                order_amount_with_rates, order_amount_discount,
                total_days, order_days_discount, order_volume,
                order_volume_discount, final_order_amount,
                customer_selection_data, False
            )
        except Exception as e:
            error = f'Ошибка генерации pdf: {e}'
            logger.error(error)
            return Response(
                {'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

    @staticmethod
    def send_order(
            customer: Customer, pdf_file_path: str
    ) -> Union[Response, None]:
        """
        Sends an order to a Telegram group and via email.

        This method sends the order details to a specified Telegram group and
        via email. If any of these operations fail, it logs the error and
        returns an HTTP 500 response with the error details.

        Args:
            customer (Customer): The customer object containing order details.
            pdf_file_path (str): The file path to the PDF document to be sent.

        Returns:
            Union[Response, None]: Returns an HTTP 500 response in case of an
                                   error, otherwise returns None.
        """

        order_info = (
            f'Заказ:\n'
            f'Название компании: {customer.company_name}\n'
            f'Имя: {customer.name}\n'
            f'Телефон: {customer.phone}\n'
            f'email: {customer.email}')
        try:
            asyncio.run(send_pdf_to_group(order_info, pdf_file_path))
        except Exception as e:
            error = f'Ошибка отправки заявки в Telegram: {e}'
            logger.error(error)
            return Response(
                {'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            send_email_with_order(order_info, pdf_file_path)
        except Exception as e:
            error = f'Ошибка отправки заявки на почту: {e}'
            logger.error(error)
            return Response(
                {'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            os.remove(pdf_file_path)
        except Exception as e:
            logger.error(f'Ошибка удаления pdf файла: {e}')

    @method_decorator(ratelimit(key='ip', rate='12/m', block=True))
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            customer_data = validated_data.pop('customer')
            customer = Customer.objects.create(**customer_data)
            city = validated_data.pop('city')
            station = validated_data.pop('station')
            block_position = validated_data.pop('block_position')
            month = validated_data.pop('month')
            customer_selection_data = validated_data.pop('customer_selection')

            (
                other_person_rate, hour_selected_rate, block_position_rate,
                month_rate
            ) = get_rates(station, block_position, month, validated_data)

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

            (
                total_days, order_volume, order_customer_selections,
                order_amount_discount, order_days_discount,
                order_volume_discount, order_amount_with_rates,
                final_order_amount
            ) = main_calculating(
                station, other_person_rate, hour_selected_rate,
                block_position_rate, month_rate, customer_selection_data,
                month, order
            )

            OrderCustomerSelection.objects.bulk_create(
                order_customer_selections
            )
            order.order_amount_discount = order_amount_discount
            order.order_days_discount = order_days_discount
            order.order_volume_discount = order_volume_discount
            order.final_order_amount = final_order_amount
            order.save()
        except Exception as e:
            error = f'Ошибка создания заказа: {e}'
            logger.error(error)
            return Response(
                {'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            pdf_file_path = create_pdf(
                city, station, month, block_position, block_position_rate,
                month_rate, other_person_rate, hour_selected_rate,
                order_amount_with_rates, order_amount_discount,
                total_days, order_days_discount, order_volume,
                order_volume_discount, final_order_amount,
                customer_selection_data, True
            )
        except Exception as e:
            error = f'Ошибка генерации pdf: {e}'
            logger.error(error)
            return Response(
                {'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        self.send_order(customer, pdf_file_path)

        return Response(status=status.HTTP_201_CREATED)
