"""Admin: Holidays CRUD."""
from rest_framework.views import APIView

from apps.notifications.models.notifications import Holiday
from apps.notifications.serializers.admin import HolidayAdminSerializer
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class HolidaysAdminListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return CustomResponse.success(
            request=request,
            data=HolidayAdminSerializer(Holiday.objects.all(), many=True).data,
        )

    def post(self, request):
        serializer = HolidayAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        holiday = serializer.save()
        return CustomResponse.created(
            request=request,
            data=HolidayAdminSerializer(holiday).data,
        )


class HolidaysAdminDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def _get(self, holiday_id):
        h = Holiday.objects.filter(id=holiday_id).first()
        if not h:
            raise CustomException("NOT_FOUND")
        return h

    def get(self, request, holiday_id):
        return CustomResponse.success(
            request=request,
            data=HolidayAdminSerializer(self._get(holiday_id)).data,
        )

    def patch(self, request, holiday_id):
        h = self._get(holiday_id)
        serializer = HolidayAdminSerializer(h, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=HolidayAdminSerializer(h).data,
        )

    def delete(self, request, holiday_id):
        self._get(holiday_id).delete()
        return CustomResponse.success(request=request, message_key="DELETED")
