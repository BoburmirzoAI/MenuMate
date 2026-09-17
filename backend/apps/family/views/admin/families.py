"""Admin: Oilalar ro'yxati va tafsilotlari."""
from django.db.models import Q
from rest_framework.views import APIView

from apps.family.models.family import FamilyProfile
from apps.family.serializers.admin import (
    FamilyAdminDetailSerializer,
    FamilyAdminListSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class FamilyAdminListAPIView(APIView):
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
        )


class FamilyAdminDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, family_id):
        family = FamilyProfile.objects.filter(id=family_id).first()
        if not family:
            raise CustomException("FAMILY_NOT_FOUND")
        return CustomResponse.success(
            request=request,
            data=FamilyAdminDetailSerializer(family).data,
        )
