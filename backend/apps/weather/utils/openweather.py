"""
OpenWeatherMap integratsiyasi.

- get_weather_for_city(city)  →  WeatherSnapshot
- 1 kunda bir marta so'raladi (cache DB'da)
- API key .env dagi OPENWEATHER_API_KEY dan olinadi
"""
import logging
from datetime import timedelta
from decimal import Decimal
from typing import Optional

import requests
from django.utils import timezone

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.weather.models.weather import WeatherSnapshot
from core import config

logger = logging.getLogger(__name__)

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
CACHE_LIFETIME_HOURS = 3  # har 3 soatda bir yangilanadi
REQUEST_TIMEOUT_SECONDS = 5


def get_weather_for_city(city: str, force_refresh: bool = False) -> WeatherSnapshot:
    """
    Shahar uchun ob-havo qaytaradi. Cache ishlaydi (3 soat).

    Args:
        city: Shahar nomi ("Tashkent", "Samarkand")
        force_refresh: Cache'ni e'tibormay yangi so'rov qilish

    Returns:
        WeatherSnapshot obyekti

    Raises:
        CustomException("WEATHER_FETCH_FAILED") — API ishlamasa
        CustomException("WEATHER_CITY_NOT_FOUND") — shahar topilmasa
    """
    city = city.strip()
    if not city:
        raise CustomException("VALIDATION_ERROR", errors={"city": "bo'sh"})

    # 1. Cache tekshirish
    if not force_refresh:
        cached = _get_cached(city)
        if cached:
            return cached

    # 2. API key mavjudmi
    api_key = config.OPENWEATHER_API_KEY
    if not api_key:
        raise CustomException(
            "WEATHER_FETCH_FAILED",
            context={"reason": "API key sozlanmagan"},
        )

    # 3. OpenWeatherMap'ga so'rov
    try:
        response = requests.get(
            OPENWEATHER_URL,
            params={
                'q': city,
                'appid': api_key,
                'units': 'metric',  # Celsius
                'lang': 'en',
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as e:
        logger.error("OpenWeatherMap request failed: %s", e)
        raise CustomException("WEATHER_FETCH_FAILED")

    if response.status_code == 404:
        raise CustomException("WEATHER_CITY_NOT_FOUND", context={"city": city})

    if response.status_code == 401:
        logger.error("OpenWeatherMap 401 — API key noto'g'ri yoki hali aktiv emas")
        raise CustomException(
            "WEATHER_FETCH_FAILED",
            context={"reason": "API key noto'g'ri yoki hali aktiv emas"},
        )

    if response.status_code != 200:
        logger.error(
            "OpenWeatherMap error: %s — %s", response.status_code, response.text[:200],
        )
        raise CustomException("WEATHER_FETCH_FAILED")

    # 4. Response'ni parse qilamiz
    data = response.json()
    return _save_snapshot(city, data)


def _get_cached(city: str) -> Optional[WeatherSnapshot]:
    """Oxirgi 3 soat ichidagi snapshot borligini tekshiradi."""
    threshold = timezone.now() - timedelta(hours=CACHE_LIFETIME_HOURS)
    return (
        WeatherSnapshot.objects
        .filter(city__iexact=city, fetched_at__gte=threshold)
        .order_by('-fetched_at')
        .first()
    )


def _save_snapshot(city: str, data: dict) -> WeatherSnapshot:
    """OpenWeatherMap javobidan WeatherSnapshot yaratadi."""
    main = data.get('main', {})
    weather_list = data.get('weather', [{}])
    description = weather_list[0].get('description', '') if weather_list else ''

    return WeatherSnapshot.objects.create(
        city=city,
        temperature=Decimal(str(main.get('temp', 0))),
        feels_like=Decimal(str(main.get('feels_like', 0))),
        humidity=main.get('humidity', 0),
        description=description[:200],
    )


# ---------------------------------------------------------------------
# Menu algoritmi uchun yordamchi
# ---------------------------------------------------------------------

def get_meal_hot_preference(temperature: Decimal) -> Optional[bool]:
    """
    Haroratdan is_hot preferences aniqlaydi.
      >25°C  → is_hot=False (salqin ovqatlar)
      <10°C  → is_hot=True  (issiq ovqatlar)
      Boshqa  → None (aralash)
    """
    t = float(temperature)
    if t >= 25:
        return False
    if t <= 10:
        return True
    return None
