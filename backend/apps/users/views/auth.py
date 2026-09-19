"""
Auth-related views: password (change/forgot/reset),
email verification, account delete.
Hammasi murakkab flow — APIView + plain Serializer.
"""
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.throttling import PasswordThrottle
from apps.shared.utils.custom_response import CustomResponse
from apps.users.serializers.auth import (
    ChangePasswordSerializer,
    ConfirmEmailVerificationSerializer,
    DeleteAccountSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    SendEmailVerificationSerializer,
)


class ChangePasswordAPIView(APIView):
    """
    POST /users/me/change-password/
    Body: { old_password, new_password, new_password_confirm }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request, message_key="PASSWORD_CHANGED", status_code=200,
        )


class ForgotPasswordAPIView(APIView):
    """
    POST /users/forgot-password/
    Emailga kod yuboradi. Xavfsizlik uchun email topilmasa ham 200 qaytadi.
    """
    permission_classes = [AllowAny]
    throttle_classes = [PasswordThrottle]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request, message_key="PASSWORD_RESET_CODE_SENT", status_code=200,
        )


class ResetPasswordAPIView(APIView):
    """
    POST /users/reset-password/
    Body: { email, code, new_password, new_password_confirm }
    """
    permission_classes = [AllowAny]
    throttle_classes = [PasswordThrottle]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Xavfsizlik: parol tiklanganida barcha refresh tokenlarni blacklist qilamiz
        self._blacklist_all_tokens(user)

        return CustomResponse.success(
            request=request, message_key="PASSWORD_RESET_SUCCESSFUL", status_code=200,
        )

    @staticmethod
    def _blacklist_all_tokens(user):
        try:
            tokens = OutstandingToken.objects.filter(user=user)
            for t in tokens:
                try:
                    RefreshToken(t.token).blacklist()
                except Exception:
                    pass
        except Exception:
            pass


class SendEmailVerificationAPIView(APIView):
    """POST /users/verify-email/send/ — tasdiqlash kodi yuborish."""
    permission_classes = [IsAuthenticated]
    serializer_class = SendEmailVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request, message_key="VERIFICATION_CODE_SENT", status_code=200,
        )


class ConfirmEmailVerificationAPIView(APIView):
    """POST /users/verify-email/confirm/ — kodni tekshirib email tasdiqlash."""
    permission_classes = [IsAuthenticated]
    serializer_class = ConfirmEmailVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request, message_key="EMAIL_VERIFIED", status_code=200,
        )


class DeleteAccountAPIView(APIView):
    """
    POST /users/me/delete/
    Body: { password, confirmation: "DELETE" }
    Soft delete — is_deleted=True, email anonymize qilinadi.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request, message_key="ACCOUNT_DELETED", status_code=200,
        )
