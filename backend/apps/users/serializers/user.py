"""
User serializerlari — barcha shaxsiy info + preferences endi User'da.
"""
from rest_framework import serializers

from apps.users.models.users import User


class UserResponseSerializer(serializers.ModelSerializer):
    """Login/register/me endpointlari uchun to'liq user."""
    full_name = serializers.CharField(read_only=True)
    referral_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'phone_number',
            'first_name', 'last_name', 'full_name',
            'birth_date', 'gender', 'avatar',
            'language', 'timezone', 'is_push_enabled',
            'is_email_verified', 'email_verified_at',
            'is_active',
            'is_onboarded',
            'referral_code',
            'created_at',
        ]
        read_only_fields = [
            'id', 'email', 'full_name',
            'is_email_verified', 'email_verified_at', 'is_active',
            'referral_code', 'created_at',
        ]

    def get_referral_code(self, obj) -> str | None:
        ref = getattr(obj, 'referral_code_obj', None)
        return ref.code if ref else None


class UserUpdateSerializer(serializers.ModelSerializer):
    """PATCH /me/ uchun — foydalanuvchi o'zgartira oladigan barcha fields."""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'phone_number',
            'birth_date', 'gender', 'avatar',
            'language', 'timezone',
            'is_push_enabled',
        ]
