"""Admin: Ob-havo cache."""
from rest_framework import serializers

from apps.weather.models.weather import WeatherSnapshot


class WeatherAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSnapshot
        fields = [
            'id',
            'city',
            'temperature', 'feels_like', 'humidity',
            'description',
            'fetched_at',
            'created_at',
        ]
