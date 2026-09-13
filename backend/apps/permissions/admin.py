from django.contrib import admin

from apps.permissions.models.permissions import Permission, Endpoint, Role
from apps.permissions.models.user_permissions import UserPermission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'codename', 'name', 'parent')
    list_filter = ('parent',)
    search_fields = ('codename', 'name')


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ('id', 'method', 'path', 'access_type', 'permission', 'is_active')
    list_filter = ('method', 'access_type', 'is_active')
    search_fields = ('path', 'name')
    list_select_related = ('permission',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    filter_horizontal = ('permissions',)


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'permission', 'granted_by', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'permission__codename')
