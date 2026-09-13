from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models.users import User
from apps.users.models.verification import VerificationCode


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ('-created_at',)
    list_display = (
        'id', 'email', 'first_name', 'last_name',
        'is_active', 'is_email_verified', 'is_onboarded',
        'language', 'created_at',
    )
    list_filter = (
        'is_active', 'is_staff', 'is_superuser',
        'is_email_verified', 'is_deleted', 'is_onboarded',
        'language', 'gender',
    )
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    readonly_fields = (
        'created_at', 'updated_at', 'last_login',
        'email_verified_at', 'deleted_at',
    )

    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone_number')}),
        ('Shaxsiy ma\'lumot', {
            'fields': ('first_name', 'last_name',
                       'birth_date', 'gender', 'avatar'),
        }),
        ('Sozlamalar', {
            'fields': ('language', 'timezone', 'is_push_enabled'),
        }),
        ('Tasdiqlash', {
            'fields': ('is_email_verified', 'email_verified_at'),
        }),
        ('Ruxsatlar', {
            'fields': ('roles', 'is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Soft delete', {'fields': ('is_deleted', 'deleted_at')}),
        ('Onboarding', {'fields': ('is_onboarded',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    filter_horizontal = ('roles', 'groups', 'user_permissions')


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'purpose', 'is_used', 'attempts', 'expires_at')
    list_filter = ('purpose', 'is_used')
    search_fields = ('user__email', 'code')
    readonly_fields = ('code', 'created_at', 'used_at')
