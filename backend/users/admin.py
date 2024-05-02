from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from .forms import MyUserChangeForm
from .models import User


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    form = MyUserChangeForm
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
        'get_group'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('password',)

    @admin.display(description='Группа')
    def get_group(self, obj):
        """Get user group"""

        if obj.is_superuser:
            return 'Администратор'
        groups = Group.objects.filter(user=obj)
        if groups:
            return ','.join([group.name for group in groups])
        return 'Обычный пользователь'


admin.site.register(Group, GroupAdmin)
