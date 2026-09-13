from django.contrib import admin

from apps.weather.models.weather import WeatherSnapshot


@admin.register(WeatherSnapshot)
class WeatherSnapshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'temperature', 'feels_like', 'humidity', 'description', 'fetched_at')
    list_filter = ('city',)
    search_fields = ('city',)
    readonly_fields = ('fetched_at',)
    date_hierarchy = 'fetched_at'
