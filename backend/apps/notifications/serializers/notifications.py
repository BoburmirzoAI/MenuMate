"""Notifications serializerlari."""
from rest_framework import serializers

from apps.notifications.models.notifications import Holiday, Notification


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'month', 'day', 'is_movable',
            'description', 'description_uz', 'description_ru', 'description_en',
        ]
        read_only_fields = fields


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'kind', 'title', 'body', 'image_url',
            'is_read', 'sent_at', 'created_at',
        ]
        read_only_fields = [
            'id', 'kind', 'title', 'body', 'image_url', 'sent_at', 'created_at',
        ]
