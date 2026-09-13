"""
FamilyProfile serializerlari.

CreateFamilySerializer — plain Serializer (validation: user'da allaqachon
oila borligini tekshiradi + is_onboarded flag'ini update qiladi).

FamilyProfileSerializer — oddiy read/update uchun ModelSerializer.
"""
from django.db import transaction
from rest_framework import serializers

from apps.family.models.family import FamilyProfile
from apps.shared.exceptions.custom_exceptions import CustomException


class FamilyProfileSerializer(serializers.ModelSerializer):
    """Oddiy read/update — ModelSerializer."""
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = FamilyProfile
        fields = [
            'id',
            'family_name',
            'city',
            'members_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'members_count', 'created_at', 'updated_at']

    def get_members_count(self, obj) -> int:
        return obj.members.count()


class CreateFamilySerializer(serializers.Serializer):
    """
    Oila yaratish. Har user'ning faqat 1 ta oilasi bo'lishi mumkin.
    Yaratilganda user.is_onboarded=True qilinadi.
    """
    family_name = serializers.CharField(max_length=100)
    city = serializers.CharField(
        max_length=100,
        help_text="Ob-havo API uchun shahar (masalan 'Tashkent')",
    )

    def validate(self, attrs):
        user = self.context['request'].user
        if hasattr(user, 'family') and user.family is not None:
            raise CustomException("FAMILY_ALREADY_EXISTS")
        return attrs

    def validate_family_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise CustomException("VALIDATION_ERROR", errors={"family_name": "bo'sh bo'lmasin"})
        return value

    def validate_city(self, value: str) -> str:
        return value.strip()

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        family = FamilyProfile.objects.create(user=user, **validated_data)
        user.mark_onboarded()
        return family
