"""Admin dashboard uchun umumiy KPI ma'lumotlari."""
from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView

from apps.devices.models.device import Device
from apps.family.models.family import FamilyProfile
from apps.menu.models.menu import Menu
from apps.notifications.models.notifications import Holiday, Notification
from apps.recipes.models.recipes import Ingredient, Recipe
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse
from apps.users.models.users import User


class DashboardStatsAPIView(APIView):
    """GET /admin/stats/ — KPI kartalar va oxirgi 30 kunlik menyu grafiga ma'lumot."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        chart_data = []
        for i in range(30):
            day_start = (now - timedelta(days=29 - i)).replace(
                hour=0, minute=0, second=0, microsecond=0,
            )
            day_end = day_start + timedelta(days=1)
            count = Menu.objects.filter(
                created_at__gte=day_start, created_at__lt=day_end,
            ).count()
            chart_data.append({'day': day_start.strftime('%d.%m'), 'menus': count})

        payload = {
            'kpi': {
                'total_users': User.objects.filter(is_deleted=False).count(),
                'active_users': User.objects.filter(is_deleted=False, is_active=True).count(),
                'total_families': FamilyProfile.objects.count(),
                'total_recipes': Recipe.objects.count(),
                'total_ingredients': Ingredient.objects.count(),
                'active_menus': Menu.objects.filter(status='ACTIVE').count(),
                'total_menus': Menu.objects.count(),
                'menus_last_30_days': Menu.objects.filter(created_at__gte=thirty_days_ago).count(),
                'total_holidays': Holiday.objects.count(),
                'total_notifications': Notification.objects.count(),
                'unread_notifications': Notification.objects.filter(is_read=False).count(),
                'total_devices': Device.objects.count(),
                'devices_with_fcm': Device.objects.exclude(fcm_token='').count(),
            },
            'chart_menus_last_30_days': chart_data,
        }
        return CustomResponse.success(request=request, data=payload, status_code=200)
