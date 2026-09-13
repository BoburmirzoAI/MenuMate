from rest_framework import serializers

from apps.weather.models.weather import WeatherSnapshot


class WeatherSnapshotSerializer(serializers.ModelSerializer):
    """Ob-havo javobi."""

    class Meta:
        model = WeatherSnapshot
        fields = [
            'id',
            'city',
            'temperature',
            'feels_like',
            'humidity',
            'description',
            'fetched_at',
        ]
        read_only_fields = fields
