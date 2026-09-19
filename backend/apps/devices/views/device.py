"""Device views — sodda: register + list + delete."""
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.devices.models.device import Device
from apps.devices.serializers.device import (
    DeviceListSerializer,
    DeviceRegisterSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.utils.custom_response import CustomResponse


class DeviceRegisterAPIView(APIView):
    """POST /devices/register/ — qurilma ma'lumotini yuborish yoki yangilash."""
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        device, _ = Device.objects.update_or_create(
            user=request.user,
            device_id=data['device_id'],
            defaults={**data, 'is_active': True},
        )
        return CustomResponse.success(
            request=request,
            data=DeviceListSerializer(device).data,
            message_key="CREATED",
            status_code=201,
        )


class UserDeviceListAPIView(ListAPIView):
    """GET /devices/ — o'z qurilmalari."""
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceListSerializer

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user, is_active=True)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return CustomResponse.success(
                request=request,
                data=self.paginator.get_paginated_data(serializer.data),
                status_code=200,
            )
        serializer = self.get_serializer(qs, many=True)
        return CustomResponse.success(request=request, data=serializer.data, status_code=200)


class DeviceDeleteAPIView(APIView):
    """DELETE /devices/<device_id>/ — bitta qurilmani o'chirish."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, device_id):
        device = Device.objects.filter(
            user=request.user, device_id=device_id,
        ).first()
        if not device:
            raise CustomException("DEVICE_NOT_FOUND", status_code=404)
        device.is_active = False
        device.save(update_fields=['is_active'])
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)
