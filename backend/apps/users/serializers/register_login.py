"""
Register va Login — plain Serializer (murakkab flow).
"""
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.models import Language
from apps.users.models.users import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    password_confirm = serializers.CharField(write_only=True)

    first_name = serializers.CharField(required=False, allow_blank=True, max_length=64)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=64)
    language = serializers.CharField(required=False, allow_blank=True, max_length=5)
    referral_code = serializers.CharField(required=False, allow_blank=True, max_length=20)

    def validate_email(self, value: str) -> str:
        value = value.strip().lower()
        if User.objects.with_deleted().filter(email__iexact=value).exists():
            raise CustomException(
                "EMAIL_ALREADY_EXISTS",
                status_code=400,
                errors={
                    "detail": f"User with email={value} already exists (including soft-deleted).",
                    "field": "email",
                    "value": value,
                    "reason": "email_already_registered",
                },
            )
        return value

    def validate_language(self, value: str) -> str:
        if not value:
            return ''
        v = value.upper()
        if v not in Language.values:
            raise CustomException(
                "INVALID_LANGUAGE_TYPE",
                status_code=400,
                errors={
                    "detail": f"Language code '{value}' is not supported; allowed: {list(Language.values)}",
                    "field": "language",
                    "value": value,
                    "allowed": list(Language.values),
                    "reason": "unsupported_language_code",
                },
            )
        return v

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise CustomException(
                "PASSWORDS_DO_NOT_MATCH",
                status_code=400,
                errors={
                    "detail": "password and password_confirm do not match",
                    "fields": ["password", "password_confirm"],
                    "reason": "password_confirm_mismatch",
                },
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm', None)

        first_name = validated_data.pop('first_name', '') or ''
        last_name = validated_data.pop('last_name', '') or ''
        language = validated_data.pop('language', '') or ''
        validated_data.pop('referral_code', None)  # hozircha ishlatilmaydi

        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            first_name=first_name,
            last_name=last_name,
            language=language or 'UZ',
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs['email'].strip().lower()
        user = User.objects.with_deleted().filter(email__iexact=email).first()

        if not user or user.is_deleted:
            raise CustomException(
                "INVALID_CREDENTIALS",
                status_code=400,
                errors={
                    "detail": f"No active user with email={email}",
                    "field": "email",
                    "reason": "user_not_found_or_deleted",
                },
            )

        if not user.is_active:
            raise CustomException(
                "USER_INACTIVE",
                status_code=403,
                errors={
                    "detail": f"User email={email} exists but is_active=False",
                    "user_id": user.pk,
                    "reason": "user_deactivated",
                },
            )

        auth_user = authenticate(username=email, password=attrs['password'])
        if not auth_user:
            raise CustomException(
                "INVALID_CREDENTIALS",
                status_code=400,
                errors={
                    "detail": f"Password check failed for email={email}",
                    "field": "password",
                    "reason": "wrong_password",
                },
            )

        attrs['user'] = auth_user
        return attrs
