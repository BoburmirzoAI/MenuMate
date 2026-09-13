"""Device serializerlari — soddalashtirilgan."""
from rest_framework import serializers

from apps.devices.models.device import Device


class DeviceRegisterSerializer(serializers.ModelSerializer):
    """
    Login/registerdan keyin mobile yuboradi:
    { device_id, device_type, fcm_token, app_version }
    """
    class Meta:
        model = Device
        fields = ['device_id', 'device_type', 'fcm_token', 'app_version']


class DeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'id', 'device_id', 'device_type', 'app_version',
            'is_active', 'last_login',
        ]
        read_only_fields = fields
