"""HealthCondition — read-only reference data."""
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.family.models.family import HealthCondition
from apps.family.serializers.health_condition import HealthConditionSerializer
from apps.shared.utils.custom_response import CustomResponse


class HealthConditionListAPIView(ListAPIView):
    """GET /family/health-conditions/ — barcha sog'liq holatlari."""
    permission_classes = [IsAuthenticated]
    serializer_class = HealthConditionSerializer
    queryset = HealthCondition.objects.all()
    pagination_class = None  # to'liq ro'yxat (kam yozuv)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        category = request.query_params.get('category')
        if category:
            qs = qs.filter(category=category.upper())

        serializer = self.get_serializer(qs, many=True)
        return CustomResponse.success(request=request, data=serializer.data)
