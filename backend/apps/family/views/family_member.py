"""
FamilyMember views.

/family/members/         — list + create
/family/members/<id>/    — retrieve + patch + delete

Barcha view'lar current user'ning oilasi ichida ishlaydi.
Boshqa oilaning a'zosiga tegib bo'lmaydi (queryset filter'i orqali).
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.family.models.family import FamilyMember, FamilyProfile
from apps.family.serializers.family_member import (
    FamilyMemberReadSerializer,
    FamilyMemberWriteSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.utils.custom_response import CustomResponse


def _get_family_or_raise(user) -> FamilyProfile:
    family = FamilyProfile.objects.filter(user=user).first()
    if not family:
        raise CustomException(
            "FAMILY_NOT_FOUND",
            status_code=404,
            errors={
                "detail": f"User user_id={user.pk} has no family profile",
                "user_id": user.pk,
                "reason": "user_has_no_family",
            },
        )
    return family


def _get_member_or_raise(family: FamilyProfile, member_id: int) -> FamilyMember:
    member = FamilyMember.objects.filter(family=family, pk=member_id).first()
    if not member:
        raise CustomException(
            "MEMBER_NOT_FOUND",
            status_code=404,
            errors={
                "detail": f"Member id={member_id} not found in family_id={family.pk}",
                "family_id": family.pk,
                "member_id": member_id,
                "reason": "member_not_found_or_wrong_family",
            },
        )
    return member


class FamilyMemberListCreateAPIView(APIView):
    """GET+POST /family/members/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = _get_family_or_raise(request.user)
        members = family.members.all().prefetch_related(
            'liked_recipes', 'disliked_recipes',
            'health_conditions', 'allergen_ingredients',
        )
        return CustomResponse.success(
            request=request,
            data=FamilyMemberReadSerializer(members, many=True).data,
            status_code=200,
        )

    def post(self, request):
        family = _get_family_or_raise(request.user)
        serializer = FamilyMemberWriteSerializer(
            data=request.data, context={'request': request, 'family': family},
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        return CustomResponse.created(
            request=request,
            message_key="MEMBER_CREATED",
            data=FamilyMemberReadSerializer(member).data,
            status_code=201,
        )


class FamilyMemberDetailAPIView(APIView):
    """GET+PATCH+DELETE /family/members/<id>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, member_id: int):
        family = _get_family_or_raise(request.user)
        member = _get_member_or_raise(family, member_id)
        return CustomResponse.success(
            request=request,
            data=FamilyMemberReadSerializer(member).data,
            status_code=200,
        )

    def patch(self, request, member_id: int):
        family = _get_family_or_raise(request.user)
        member = _get_member_or_raise(family, member_id)

        serializer = FamilyMemberWriteSerializer(
            data=request.data,
            context={'request': request, 'family': family},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.update(member, serializer.validated_data)
        return CustomResponse.success(
            request=request,
            message_key="UPDATED",
            data=FamilyMemberReadSerializer(member).data,
            status_code=200,
        )

    def delete(self, request, member_id: int):
        family = _get_family_or_raise(request.user)
        member = _get_member_or_raise(family, member_id)
        member.delete()
        return CustomResponse.success(
            request=request, message_key="MEMBER_DELETED", status_code=200,
        )
