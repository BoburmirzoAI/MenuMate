from django.urls import path

from apps.weather.views.weather import WeatherAPIView

app_name = 'weather'

urlpatterns = [
    path('', WeatherAPIView.as_view(), name='current'),
]
