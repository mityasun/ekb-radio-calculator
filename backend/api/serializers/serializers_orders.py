from rest_framework import serializers

from api.serializers.serializers_customers import CustomerSerializer
from orders.models import Order, OrderCustomerSelection
from rates.models import BlockPosition
from settings.models import City, Month, AudioDuration, TimeInterval
from stations.models import RadioStation


class CustomerSelectionSerializer(serializers.ModelSerializer):
    """Serializer for the customer selection"""

    date = serializers.IntegerField(required=True)
    time_interval = serializers.PrimaryKeyRelatedField(
        queryset=TimeInterval.objects.all(), required=True
    )
    audio_duration = serializers.PrimaryKeyRelatedField(
        queryset=AudioDuration.objects.all(), required=True
    )

    class Meta:
        model = OrderCustomerSelection
        exclude = ('order', 'week_day', 'interval_price')
        read_only_fields = ('order', 'week_day', 'interval_price')


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for create order"""

    customer = CustomerSerializer()
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), required=True
    )
    station = serializers.PrimaryKeyRelatedField(
        queryset=RadioStation.objects.all(), required=True
    )
    block_position = serializers.PrimaryKeyRelatedField(
        queryset=BlockPosition.objects.all(), required=True
    )
    month = serializers.PrimaryKeyRelatedField(
        queryset=Month.objects.all(), required=True
    )
    other_person_rate = serializers.BooleanField(required=True)
    hour_selected_rate = serializers.BooleanField(required=True)
    customer_selection = CustomerSelectionSerializer(
        source='ordercustomerselection_set', many=True, read_only=True
    )

    class Meta:
        model = Order
        exclude = (
            'created_at', 'block_position_rate', 'month_rate', 'order_amount',
            'total_days', 'order_volume', 'final_order_amount'
        )
        read_only_fields = (
            'created_at', 'block_position_rate', 'month_rate', 'order_amount',
            'total_days', 'order_volume', 'final_order_amount'
        )

    def validate(self, data):
        """Validate initial_data"""

        if 'customer_selection' in self.initial_data:
            data['customer_selection'] = self.initial_data.get(
                'customer_selection'
            )
        return data
