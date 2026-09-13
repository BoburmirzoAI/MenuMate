"""
FamilyProfile views.

Bitta user = bitta oila → /family/ (id kerak emas).
GET  → o'z oilasini olish (yoki 404)
POST → yaratish (bir marta)
PATCH → yangilash
DELETE → o'chirish (a'zolar ham cascade)
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.family.models.family import FamilyProfile
from apps.family.serializers.family_profile import (
    CreateFamilySerializer,
    FamilyProfileSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.utils.custom_response import CustomResponse


class FamilyProfileAPIView(APIView):
    """GET/POST/PATCH/DELETE /family/"""
    permission_classes = [IsAuthenticated]

    def _get_family(self, user):
        family = FamilyProfile.objects.filter(user=user).first()
        if not family:
            raise CustomException("FAMILY_NOT_FOUND")
        return family

    # ------------- GET -------------
    def get(self, request):
        family = self._get_family(request.user)
        return CustomResponse.success(
            request=request, data=FamilyProfileSerializer(family).data,
        )

    # ------------- POST -------------
    def post(self, request):
        serializer = CreateFamilySerializer(
            data=request.data, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        family = serializer.save()
        return CustomResponse.created(
            request=request,
            message_key="FAMILY_CREATED",
            data=FamilyProfileSerializer(family).data,
        )

    # ------------- PATCH -------------
    def patch(self, request):
        family = self._get_family(request.user)
        serializer = FamilyProfileSerializer(family, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request, data=serializer.data, message_key="UPDATED",
        )

    # ------------- DELETE -------------
    def delete(self, request):
        family = self._get_family(request.user)
        family.delete()
        # Foydalanuvchi qayta oila yaratishi mumkin — is_onboarded'ni qaytarish
        request.user.is_onboarded = False
        request.user.save(update_fields=['is_onboarded'])
        return CustomResponse.success(
            request=request, message_key="FAMILY_DELETED",
        )
