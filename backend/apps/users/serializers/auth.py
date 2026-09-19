"""
Auth serializerlari — password (change/forgot/reset), email verify, delete.
"""
import logging

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.users.models.users import User
from apps.users.models.verification import VerificationCode

logger = logging.getLogger(__name__)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.validated_data['refresh'])
            token.blacklist()
        except TokenError:
            raise CustomException(
                "INVALID_TOKEN",
                status_code=401,
                errors={
                    "detail": "Refresh token is invalid, expired or already blacklisted",
                    "field": "refresh",
                    "reason": "refresh_token_invalid_or_expired",
                },
            )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user: User = self.context['request'].user

        if not user.check_password(attrs['old_password']):
            raise CustomException(
                "INVALID_OLD_PASSWORD",
                status_code=400,
                errors={
                    "detail": f"Old password check failed for user_id={user.pk}",
                    "field": "old_password",
                    "user_id": user.pk,
                    "reason": "wrong_old_password",
                },
            )

        if attrs['new_password'] != attrs['new_password_confirm']:
            raise CustomException(
                "PASSWORDS_DO_NOT_MATCH",
                status_code=400,
                errors={
                    "detail": "new_password and new_password_confirm do not match",
                    "fields": ["new_password", "new_password_confirm"],
                    "reason": "password_confirm_mismatch",
                },
            )

        if attrs['old_password'] == attrs['new_password']:
            raise CustomException(
                "NEW_PASSWORD_SAME_AS_OLD",
                status_code=400,
                errors={
                    "detail": "new_password must differ from old_password",
                    "fields": ["old_password", "new_password"],
                    "user_id": user.pk,
                    "reason": "new_password_same_as_old",
                },
            )

        try:
            validate_password(attrs['new_password'], user=user)
        except DjangoValidationError as e:
            raise CustomException(
                "WEAK_PASSWORD",
                status_code=400,
                errors={
                    "detail": f"Password rejected by Django validators: {list(e.messages)}",
                    "field": "new_password",
                    "user_id": user.pk,
                    "violations": list(e.messages),
                    "reason": "password_fails_strength_rules",
                },
            )

        return attrs

    def save(self, **kwargs):
        user: User = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        email = self.validated_data['email'].strip().lower()
        user = User.objects.filter(email__iexact=email, is_active=True).first()

        if user:
            code = VerificationCode.generate(
                user=user,
                purpose=VerificationCode.Purpose.PASSWORD_RESET,
                destination=user.email,
                lifetime_minutes=15,
            )
            logger.info(
                "PASSWORD_RESET code for %s: %s", user.email, code.code,
            )


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs['email'].strip().lower()
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if not user:
            raise CustomException(
                "INVALID_VERIFICATION_CODE",
                status_code=400,
                errors={
                    "detail": f"No active user for email={email}",
                    "field": "email",
                    "reason": "user_not_found_for_reset",
                },
            )

        code_obj = VerificationCode.objects.filter(
            user=user,
            purpose=VerificationCode.Purpose.PASSWORD_RESET,
            is_used=False,
        ).order_by('-created_at').first()

        if not code_obj or not code_obj.verify(attrs['code']):
            raise CustomException(
                "INVALID_VERIFICATION_CODE",
                status_code=400,
                errors={
                    "detail": f"No unused/valid PASSWORD_RESET code for user_id={user.pk}",
                    "field": "code",
                    "user_id": user.pk,
                    "reason": "verification_code_invalid_or_expired",
                },
            )

        if attrs['new_password'] != attrs['new_password_confirm']:
            raise CustomException(
                "PASSWORDS_DO_NOT_MATCH",
                status_code=400,
                errors={
                    "detail": "new_password and new_password_confirm do not match",
                    "fields": ["new_password", "new_password_confirm"],
                    "reason": "password_confirm_mismatch",
                },
            )

        try:
            validate_password(attrs['new_password'], user=user)
        except DjangoValidationError as e:
            raise CustomException(
                "WEAK_PASSWORD",
                status_code=400,
                errors={
                    "detail": f"Password rejected by Django validators: {list(e.messages)}",
                    "field": "new_password",
                    "user_id": user.pk,
                    "violations": list(e.messages),
                    "reason": "password_fails_strength_rules",
                },
            )

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class SendEmailVerificationSerializer(serializers.Serializer):
    def save(self, **kwargs):
        user: User = self.context['request'].user
        if user.is_email_verified:
            raise CustomException(
                "EMAIL_ALREADY_VERIFIED",
                status_code=400,
                errors={
                    "detail": f"Email for user_id={user.pk} is already verified",
                    "user_id": user.pk,
                    "email": user.email,
                    "reason": "email_already_verified",
                },
            )

        code = VerificationCode.generate(
            user=user,
            purpose=VerificationCode.Purpose.EMAIL_VERIFY,
            destination=user.email,
            lifetime_minutes=15,
        )
        # DEV vaqtincha: kodni log'ga yozamiz. Production'da email service (celery task) bilan almashtiriladi.
        logger.warning(
            "EMAIL_VERIFY code for %s: %s", user.email, code.code,
        )


class ConfirmEmailVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        user: User = self.context['request'].user
        if user.is_email_verified:
            raise CustomException(
                "EMAIL_ALREADY_VERIFIED",
                status_code=400,
                errors={
                    "detail": f"Email for user_id={user.pk} is already verified",
                    "user_id": user.pk,
                    "email": user.email,
                    "reason": "email_already_verified",
                },
            )

        code_obj = VerificationCode.objects.filter(
            user=user,
            purpose=VerificationCode.Purpose.EMAIL_VERIFY,
            is_used=False,
        ).order_by('-created_at').first()

        if not code_obj or not code_obj.verify(attrs['code']):
            raise CustomException(
                "INVALID_VERIFICATION_CODE",
                status_code=400,
                errors={
                    "detail": f"No unused/valid EMAIL_VERIFY code for user_id={user.pk}",
                    "field": "code",
                    "user_id": user.pk,
                    "reason": "verification_code_invalid_or_expired",
                },
            )

        return attrs

    def save(self, **kwargs):
        user: User = self.context['request'].user
        user.verify_email()
        return user


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirmation = serializers.CharField()

    def validate(self, attrs):
        user: User = self.context['request'].user
        if attrs['confirmation'] != 'DELETE':
            raise CustomException(
                "DELETE_CONFIRMATION_INVALID",
                status_code=400,
                errors={
                    "detail": "confirmation must be exactly the literal 'DELETE'",
                    "field": "confirmation",
                    "expected": "DELETE",
                    "reason": "confirmation_literal_mismatch",
                },
            )
        if not user.check_password(attrs['password']):
            raise CustomException(
                "INVALID_PASSWORD",
                status_code=400,
                errors={
                    "detail": f"Password check failed for user_id={user.pk}",
                    "field": "password",
                    "user_id": user.pk,
                    "reason": "wrong_password",
                },
            )
        return attrs

    def save(self, **kwargs):
        self.context['request'].user.soft_delete()
