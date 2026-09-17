"""Devices admin URL'lari."""
from django.urls import path

from apps.devices.views.admin import DevicesAdminListAPIView

app_name = 'devices-admin'

urlpatterns = [
    path('', DevicesAdminListAPIView.as_view(), name='list'),
]
