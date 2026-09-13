from django.urls import path

from apps.devices.views.device import (
    DeviceDeleteAPIView,
    DeviceRegisterAPIView,
    UserDeviceListAPIView,
)
from apps.devices.views.version import VersionCheckAPIView

app_name = 'devices'

urlpatterns = [
    path('version-check/', VersionCheckAPIView.as_view(), name='version-check'),
    path('', UserDeviceListAPIView.as_view(), name='device-list'),
    path('register/', DeviceRegisterAPIView.as_view(), name='device-register'),
    path('<str:device_id>/', DeviceDeleteAPIView.as_view(), name='device-delete'),
]
