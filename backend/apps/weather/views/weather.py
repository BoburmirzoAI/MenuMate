"""
Weather API.

GET /weather/                — oila shahri uchun ob-havo (default)
GET /weather/?city=Samarkand — muayyan shahar
GET /weather/?refresh=true   — cache'ni e'tibormay yangi so'rov
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.family.models.family import FamilyProfile
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.utils.custom_response import CustomResponse
from apps.weather.serializers.weather import WeatherSnapshotSerializer
from apps.weather.utils.openweather import get_weather_for_city


class WeatherAPIView(APIView):
    """GET /weather/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = request.query_params.get('city')

        # Shahar berilmasa — oila shahridan olamiz
        if not city:
            family = FamilyProfile.objects.filter(user=request.user).first()
            if not family:
                raise CustomException("FAMILY_NOT_FOUND")
            city = family.city

        if not city:
            raise CustomException(
                "VALIDATION_ERROR",
                errors={"city": "shahar ko'rsatilmagan"},
            )

        force = request.query_params.get('refresh', '').lower() in ('true', '1')

        snapshot = get_weather_for_city(city, force_refresh=force)

        return CustomResponse.success(
            request=request,
            data=WeatherSnapshotSerializer(snapshot).data,
        )
