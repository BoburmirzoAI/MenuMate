"""Notifications admin URL'lari."""
from django.urls import path

from apps.notifications.views.admin import (
    BroadcastAPIView,
    HolidaysAdminDetailAPIView,
    HolidaysAdminListCreateAPIView,
    NotificationsAdminListAPIView,
)

app_name = 'notifications-admin'

urlpatterns = [
    path('holidays/', HolidaysAdminListCreateAPIView.as_view(), name='holidays-list'),
    path('holidays/<int:holiday_id>/', HolidaysAdminDetailAPIView.as_view(), name='holidays-detail'),
    path('', NotificationsAdminListAPIView.as_view(), name='notifications-list'),
    path('broadcast/', BroadcastAPIView.as_view(), name='broadcast'),
]
