from django.contrib import admin

from customers.models import Customer


@admin.register(Customer)
class OrderAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'name', 'phone', 'email')
    search_fields = ('company_name', 'name', 'phone', 'email')
