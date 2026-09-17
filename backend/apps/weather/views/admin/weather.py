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
        )

    def delete(self, request):
        # Cache'dan barcha ob-havo yozuvlari o'chirish uchun eng oddiy usul
        WeatherSnapshot.objects.all().delete()
        # Redis cache'dagi lookup key'larni ham tozalaymiz
        try:
            cache.delete_pattern('weather:*')  # django-redis extension
        except AttributeError:
            pass
        return CustomResponse.success(request=request, message_key="OK")
