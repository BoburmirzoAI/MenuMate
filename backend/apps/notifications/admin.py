from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.notifications.models.notifications import Holiday, Notification


@admin.register(Holiday)
class HolidayAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name', 'month', 'day', 'is_movable')
    list_filter = ('is_movable', 'month')
    search_fields = ('name',)
    ordering = ('month', 'day')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'kind', 'title', 'is_read', 'created_at')
    list_filter = ('kind', 'is_read')
    search_fields = ('user__email', 'title', 'body')
    list_select_related = ('user',)
    readonly_fields = ('created_at', 'sent_at')
