from django.contrib import admin

from discounts.models import (VolumeDiscount, DaysDiscount,
                              AmountDiscount)
from rates.models import MonthRate, BlockPositionRate, IntervalPrice
from stations.models import (RadioStation,
                             AudienceSexStation, AudienceAgeStation)


class AudienceSexStationInline(admin.TabularInline):
    model = AudienceSexStation
    min_num = 1
    extra = 1
    classes = ('collapse',)
    autocomplete_fields = ('sex',)
    fields = ('id', 'sex', 'percent')


class AudienceAgeStationInline(admin.TabularInline):
    model = AudienceAgeStation
    min_num = 0
    extra = 1
    classes = ('collapse',)
    autocomplete_fields = ('age',)
    fields = ('id', 'age', 'percent')


class MonthRateInline(admin.TabularInline):
    model = MonthRate
    min_num = 1
    extra = 0
    classes = ('collapse',)
    autocomplete_fields = ('month',)
    fields = ('id', 'month', 'rate')


class BlockPositionRateInline(admin.TabularInline):
    model = BlockPositionRate
    min_num = 1
    extra = 0
    classes = ('collapse',)
    autocomplete_fields = ('block_position',)
    fields = ('id', 'block_position', 'rate')


class IntervalPriceInline(admin.TabularInline):
    model = IntervalPrice
    min_num = 1
    extra = 0
    classes = ('collapse',)
    autocomplete_fields = ('time_interval', 'audio_duration')
    fields = ('id', 'time_interval', 'audio_duration', 'interval_price')


class AmountDiscountInline(admin.TabularInline):
    model = AmountDiscount
    min_num = 1
    extra = 0
    classes = ('collapse',)
    fields = ('id', 'order_amount', 'discount')


class DaysDiscountInline(admin.TabularInline):
    model = DaysDiscount
    min_num = 1
    extra = 0
    classes = ('collapse',)
    fields = ('id', 'total_days', 'discount')


class VolumeDiscountInline(admin.TabularInline):
    model = VolumeDiscount
    min_num = 1
    extra = 0
    classes = ('collapse',)
    fields = ('id', 'order_volume', 'discount')


@admin.register(RadioStation)
class StationsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'city', 'reach_dly', 'reach_dly_percent',
        'other_person_rate', 'hour_selected_rate', 'default'
    )
    search_fields = ('id', 'name', 'city', 'description')
    list_filter = ('city',)
    autocomplete_fields = ('city',)
    # prepopulated_fields = {
    #     'slug': ['name'], 'seo_title': ['name'], 'seo_img_alt': ['name'],
    #     'seo_description': ['description']
    # }
    # readonly_fields = ('avg_rating', 'amount_votes', 'images_preview')
    # formfield_overrides = {
    #     models.CharField: {
    #         'widget': forms.Textarea(attrs={'rows': 1, 'cols': 150})
    #     },
    #     models.TextField: {
    #         'widget': forms.Textarea(attrs={'rows': 10, 'cols': 150})
    #     },
    # }
    inlines = [
        AudienceSexStationInline, AudienceAgeStationInline,
        MonthRateInline, BlockPositionRateInline, IntervalPriceInline,
        AmountDiscountInline, DaysDiscountInline, VolumeDiscountInline
    ]
