"""Admin: qurilmalar ro'yxati."""
from django.db.models import Q
from rest_framework.views import APIView

from apps.devices.models.device import Device
from apps.devices.serializers.admin import DeviceAdminSerializer
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class DevicesAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Device.objects.select_related('user').order_by('-last_login')

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(user__email__icontains=search) | Q(device_id__icontains=search),
            )

        device_type = request.query_params.get('device_type')
        if device_type in ('ANDROID', 'IOS', 'WEB'):
            qs = qs.filter(device_type=device_type)

        return CustomResponse.success(
            request=request,
            data=DeviceAdminSerializer(qs, many=True).data,
            status_code=200,
        )
