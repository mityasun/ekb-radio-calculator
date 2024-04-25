from django.contrib import admin

from orders.models import Order, OrderCustomerSelection


class OrderCustomerSelectionInline(admin.TabularInline):
    model = OrderCustomerSelection
    min_num = 1
    extra = 1
    classes = ('collapse',)
    autocomplete_fields = ('week_day', 'time_interval', 'audio_duration')
    fields = (
        'id', 'date', 'week_day', 'time_interval', 'audio_duration',
        'interval_price'
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    inlines = [OrderCustomerSelectionInline]
