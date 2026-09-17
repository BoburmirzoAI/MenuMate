"""Permissions admin URL'lari."""
from django.urls import path

from apps.permissions.views.admin import (
    EndpointsAdminListAPIView,
    PermissionsAdminListAPIView,
    RolesAdminDetailAPIView,
    RolesAdminListAPIView,
)

app_name = 'permissions-admin'

urlpatterns = [
    path('roles/', RolesAdminListAPIView.as_view(), name='roles-list'),
    path('roles/<int:role_id>/', RolesAdminDetailAPIView.as_view(), name='roles-detail'),
    path('permissions/', PermissionsAdminListAPIView.as_view(), name='permissions-list'),
    path('endpoints/', EndpointsAdminListAPIView.as_view(), name='endpoints-list'),
]
