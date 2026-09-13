from django.contrib import admin

from apps.devices.models.app_version import AppVersion, VersionPolicy
from apps.devices.models.device import Device


@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'version_number', 'version_code', 'release_date', 'is_active')
    list_filter = ('platform', 'is_active')
    search_fields = ('version_number',)
    readonly_fields = ('version_code',)


@admin.register(VersionPolicy)
class VersionPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'current_version', 'min_required_version', 'min_os_version')
    list_filter = ('platform',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'device_type', 'app_version', 'is_active', 'last_login')
    list_filter = ('device_type', 'is_active')
    search_fields = ('user__email', 'device_id')
    list_select_related = ('user',)
