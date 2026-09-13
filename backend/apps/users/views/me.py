"""
Me — o'z profilingizni ko'rish va o'zgartirish (bitta endpoint).
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.shared.utils.custom_response import CustomResponse
from apps.users.serializers.user import (
    UserResponseSerializer,
    UserUpdateSerializer,
)


class MeAPIView(APIView):
    """GET/PATCH /users/me/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return CustomResponse.success(
            request=request,
            data=UserResponseSerializer(request.user).data,
        )

    def patch(self, request):
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            message_key="UPDATED",
            data=UserResponseSerializer(request.user).data,
        )
