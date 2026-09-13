"""Sog'liq holatlari — reference (read-only)."""
from rest_framework import serializers

from apps.family.models.family import HealthCondition


class HealthConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCondition
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'category',
            'description', 'description_uz', 'description_ru', 'description_en',
        ]
        read_only_fields = fields
