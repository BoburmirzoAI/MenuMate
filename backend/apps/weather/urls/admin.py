"""Weather admin URL'lari."""
from django.urls import path

from apps.weather.views.admin import WeatherAdminListAPIView

app_name = 'weather-admin'

urlpatterns = [
    path('', WeatherAdminListAPIView.as_view(), name='list'),
]
