"""Admin: Qurilmalar."""
from rest_framework import serializers

from apps.devices.models.device import Device


class DeviceAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    fcm_token_set = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = [
            'id',
            'user', 'user_email',
            'device_id', 'device_type',
            'app_version',
            'is_active',
            'fcm_token_set',
            'last_login',
            'created_at',
        ]

    def get_fcm_token_set(self, obj) -> bool:
        return bool(obj.fcm_token)
