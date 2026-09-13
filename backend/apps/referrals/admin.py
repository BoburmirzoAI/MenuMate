from django.contrib import admin

from apps.referrals.models.referral import ReferralCode


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'user__email')
