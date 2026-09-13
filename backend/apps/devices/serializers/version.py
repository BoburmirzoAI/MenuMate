from rest_framework import serializers

from apps.shared.models import DeviceType


class VersionCheckSerializer(serializers.Serializer):
    """
    Mobile ilova app start'da yuboradi:
    {
        "platform": "IOS" | "ANDROID",
        "app_version": "1.2.3",
        "os_version": "15.2"          // optional
    }
    """
    platform = serializers.ChoiceField(choices=DeviceType.choices)
    app_version = serializers.CharField(max_length=20)
    os_version = serializers.CharField(max_length=20, required=False, allow_blank=True)
