"""Register + Login + Logout views."""
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.utils.custom_response import CustomResponse
from apps.users.serializers.auth import LogoutSerializer
from apps.users.serializers.register_login import (
    LoginSerializer,
    RegisterSerializer,
)
from apps.users.serializers.user import UserResponseSerializer


def _tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return CustomResponse.created(
            request=request,
            message_key="USER_REGISTERED_SUCCESSFULLY",
            data={
                'user': UserResponseSerializer(user).data,
                'tokens': _tokens_for(user),
            },
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return CustomResponse.success(
            request=request,
            message_key="LOGIN_SUCCESSFUL",
            data={
                'user': UserResponseSerializer(user).data,
                'tokens': _tokens_for(user),
            },
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request, message_key="LOGOUT_SUCCESSFUL",
        )
