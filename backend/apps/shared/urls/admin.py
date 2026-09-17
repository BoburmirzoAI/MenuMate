"""Shared admin URL'lari — stats va tizim holati."""
from django.urls import path

from apps.shared.views.admin import DashboardStatsAPIView

app_name = 'shared-admin'

urlpatterns = [
    path('stats/', DashboardStatsAPIView.as_view(), name='stats'),
]
