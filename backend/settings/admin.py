from django.contrib import admin, messages
from django.contrib.admin import sites
from django.utils.html import format_html

from settings.models import (
    City, AudioDuration, TimeInterval, AudienceSex, AudienceAge, Month,
    SystemText, WeekDay, ExcelImport
)
from utils.utils import ImportFromXLSX


class MyAdminSite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            'orders': 0,
            'customers': 1,
            'stations': 2,
            'settings': 3,
            'rates': 4,
            'users': 5,
            'auth': 6,
        }

        app_dict = self._build_app_dict(request, app_label)
        sorted_data = sorted(
            app_dict.items(), key=lambda x: ordering.get(x[0])
        )
        app_list = [value for key, value in sorted_data]

        return app_list


mysite = MyAdminSite()
admin.site = mysite
sites.site = mysite
admin.site.site_header = 'ekb-radio calculator'


@admin.register(SystemText)
class SystemTextAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(ExcelImport)
class ExcelImport(admin.ModelAdmin):
    list_display = ('id',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        excel_file_path = obj.excel_file.path
        assistant = ImportFromXLSX(excel_file_path)
        printed_text = assistant.process_all()
        formatted_printed_text = printed_text.replace('\n', '<br>')
        self.message_user(
            request, format_html(formatted_printed_text), level=messages.INFO
        )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'default')
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
    list_display = ('id', 'audio_duration', 'default')
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
