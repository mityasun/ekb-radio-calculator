from django.contrib import admin

from settings.models import (
    City, AudioDuration, TimeInterval, AudienceSex, AudienceAge, Month,
    SystemText, WeekDay
)


@admin.register(SystemText)
class SystemTextAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'month')
    search_fields = ('month',)


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'week_day')
    search_fields = ('week_day',)


@admin.register(AudioDuration)
class AudioDurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_duration')
    search_fields = ('audio_duration',)


@admin.register(TimeInterval)
class TimeIntervalAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_interval')
    search_fields = ('time_interval',)


@admin.register(AudienceSex)
class AudienceSexAdmin(admin.ModelAdmin):
    list_display = ('id', 'sex')
    search_fields = ('sex',)


@admin.register(AudienceAge)
class AudienceAgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'age')
    search_fields = ('age',)
