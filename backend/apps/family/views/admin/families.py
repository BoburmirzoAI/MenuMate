"""Admin: Oilalar ro'yxati, tafsilotlari va a'zolar boshqaruvi."""
from django.db.models import Q
from rest_framework.views import APIView

from apps.family.models.family import FamilyMember, FamilyProfile
from apps.family.serializers.admin import (
    FamilyAdminCreateSerializer,
    FamilyAdminDetailSerializer,
    FamilyAdminListSerializer,
    FamilyAdminUpdateSerializer,
    FamilyMemberAdminSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class FamilyAdminListAPIView(APIView):
    """GET/POST /admin/families/"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = FamilyProfile.objects.select_related('user').prefetch_related('members').order_by('-created_at')

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(family_name__icontains=search)
                | Q(city__icontains=search)
                | Q(user__email__icontains=search),
            )

        return CustomResponse.success(
            request=request,
            data=FamilyAdminListSerializer(qs, many=True).data,
            status_code=200,
        )

    def post(self, request):
        serializer = FamilyAdminCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        family = serializer.save()
        return CustomResponse.created(
            request=request,
            data=FamilyAdminDetailSerializer(family).data,
            status_code=201,
        )


class FamilyAdminDetailAPIView(APIView):
    """GET/PATCH/DELETE /admin/families/<id>/"""
    permission_classes = [IsAdminUser]

    def _get(self, family_id) -> FamilyProfile:
        family = FamilyProfile.objects.filter(id=family_id).first()
        if not family:
            raise CustomException("FAMILY_NOT_FOUND", status_code=404)
        return family

    def get(self, request, family_id):
        return CustomResponse.success(
            request=request,
            data=FamilyAdminDetailSerializer(self._get(family_id)).data,
            status_code=200,
        )

    def patch(self, request, family_id):
        family = self._get(family_id)
        serializer = FamilyAdminUpdateSerializer(family, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=FamilyAdminDetailSerializer(family).data,
            status_code=200,
        )

    def delete(self, request, family_id):
        family = self._get(family_id)
        family.delete()
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)


class FamilyMembersAdminListAPIView(APIView):
    """GET/POST /admin/families/<family_id>/members/"""
    permission_classes = [IsAdminUser]

    def get(self, request, family_id):
        if not FamilyProfile.objects.filter(id=family_id).exists():
            raise CustomException("FAMILY_NOT_FOUND", status_code=404)
        qs = FamilyMember.objects.filter(family_id=family_id).prefetch_related('health_conditions')
        return CustomResponse.success(
            request=request,
            data=FamilyMemberAdminSerializer(qs, many=True).data,
            status_code=200,
        )

    def post(self, request, family_id):
        if not FamilyProfile.objects.filter(id=family_id).exists():
            raise CustomException("FAMILY_NOT_FOUND", status_code=404)
        data = {**request.data, 'family': family_id}
        serializer = FamilyMemberAdminSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        return CustomResponse.created(
            request=request,
            data=FamilyMemberAdminSerializer(member).data,
            status_code=201,
        )


class FamilyMemberDetailAdminAPIView(APIView):
    """GET/PATCH/DELETE /admin/families/<family_id>/members/<member_id>/"""
    permission_classes = [IsAdminUser]

    def _get(self, family_id, member_id) -> FamilyMember:
        member = FamilyMember.objects.filter(id=member_id, family_id=family_id).first()
        if not member:
            raise CustomException("NOT_FOUND", status_code=404)
        return member

    def get(self, request, family_id, member_id):
        return CustomResponse.success(
            request=request,
            data=FamilyMemberAdminSerializer(self._get(family_id, member_id)).data,
            status_code=200,
        )

    def patch(self, request, family_id, member_id):
        member = self._get(family_id, member_id)
        serializer = FamilyMemberAdminSerializer(member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=FamilyMemberAdminSerializer(member).data,
            status_code=200,
        )

    def delete(self, request, family_id, member_id):
        self._get(family_id, member_id).delete()
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)
