"""Admin: ob-havo cache holati va tozalash."""
from django.core.cache import cache
from rest_framework.views import APIView

from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse
from apps.weather.models.weather import WeatherSnapshot
from apps.weather.serializers.admin import WeatherAdminSerializer


class WeatherAdminListAPIView(APIView):
    """GET/DELETE — cache holati va tozalash."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = WeatherSnapshot.objects.order_by('-fetched_at')[:50]
        return CustomResponse.success(
            request=request,
            data=WeatherAdminSerializer(qs, many=True).data,
            status_code=200,
        )

    def delete(self, request):
        WeatherSnapshot.objects.all().delete()
        # django-redis kengaytmasi: mos key pattern'ni tozalaydi
        try:
            cache.delete_pattern('weather:*')
        except AttributeError:
            pass
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)
