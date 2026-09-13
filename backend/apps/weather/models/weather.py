from django.db import models

from apps.shared.models import BaseModel


class WeatherSnapshot(BaseModel):
    """
    OpenWeatherMap-dan olingan cache — bir kunda bir necha marta so'ramaslik uchun.
    """
    city = models.CharField(max_length=100, db_index=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=200)
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weather_snapshot'
        ordering = ['-fetched_at']

    def __str__(self):
        return f"{self.city} — {self.temperature}°C"
