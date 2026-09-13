from django.contrib import admin

from apps.shared.models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_type', 'original_name', 'size', 'created_at')
    list_filter = ('file_type',)
    search_fields = ('original_name',)
