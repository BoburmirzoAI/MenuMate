"""Admin: Bayramlar va bildirishnomalar."""
from rest_framework import serializers

from apps.notifications.models.notifications import Holiday, Notification


class HolidayAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'month', 'day',
            'is_movable',
            'description',
        ]


class NotificationAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'user', 'user_email',
            'kind',
            'title', 'body', 'image_url',
            'is_read', 'sent_at',
            'created_at',
        ]


class BroadcastNotificationSerializer(serializers.Serializer):
    """Barcha faol foydalanuvchilarga xabar yuborish uchun ma'lumot."""
    title = serializers.CharField(max_length=200)
    body = serializers.CharField()
    kind = serializers.ChoiceField(
        choices=Notification.Kind.choices,
        default=Notification.Kind.GENERAL,
    )
    image_url = serializers.URLField(required=False, allow_blank=True)
