from django.contrib import admin

from rates.models import BlockPosition


@admin.register(BlockPosition)
class BlockPositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'block_position')
    search_fields = ('block_position',)
