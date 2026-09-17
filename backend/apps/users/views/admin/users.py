"""Admin panel: foydalanuvchilarni ko'rish va boshqarish."""
from django.db.models import Q
from rest_framework.views import APIView

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse
from apps.users.models.users import User
from apps.users.serializers.admin import (
    UserAdminDetailSerializer,
    UserAdminListSerializer,
    UserAdminUpdateSerializer,
)


class UsersAdminListAPIView(APIView):
    """GET /admin/users/ — filter: search, status."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = User.objects.filter(is_deleted=False).prefetch_related('roles').order_by('-created_at')

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search),
            )

        status = request.query_params.get('status')
        if status == 'active':
            qs = qs.filter(is_active=True)
        elif status == 'blocked':
            qs = qs.filter(is_active=False)
        elif status == 'unverified':
            qs = qs.filter(is_email_verified=False)

        return CustomResponse.success(
            request=request,
            data=UserAdminListSerializer(qs, many=True).data,
        )


class UsersAdminDetailAPIView(APIView):
    """GET/PATCH/DELETE /admin/users/<id>/"""
    permission_classes = [IsAdminUser]

    def _get(self, user_id: int) -> User:
        user = User.objects.filter(id=user_id, is_deleted=False).first()
        if not user:
            raise CustomException("USER_NOT_FOUND")
        return user

    def get(self, request, user_id):
        user = self._get(user_id)
        return CustomResponse.success(
            request=request,
            data=UserAdminDetailSerializer(user).data,
        )

    def patch(self, request, user_id):
        user = self._get(user_id)
        serializer = UserAdminUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=UserAdminDetailSerializer(user).data,
        )

    def delete(self, request, user_id):
        user = self._get(user_id)
        # Superuser'ni o'chirmaymiz
        if user.is_superuser:
            raise CustomException("VALIDATION_ERROR", errors={"detail": "Superuser o'chirilmaydi"})
        user.soft_delete() if hasattr(user, 'soft_delete') else user.delete()
        return CustomResponse.success(request=request, message_key="DELETED")
