"""Permissions admin URL'lari."""
from django.urls import path

from apps.permissions.views.admin import (
    EndpointsAdminDetailAPIView,
    EndpointsAdminListAPIView,
    PermissionsAdminDetailAPIView,
    PermissionsAdminListAPIView,
    RolesAdminDetailAPIView,
    RolesAdminListAPIView,
)

app_name = 'permissions-admin'

urlpatterns = [
    path('roles/', RolesAdminListAPIView.as_view(), name='roles-list'),
    path('roles/<int:role_id>/', RolesAdminDetailAPIView.as_view(), name='roles-detail'),
    path('permissions/', PermissionsAdminListAPIView.as_view(), name='permissions-list'),
    path('permissions/<int:perm_id>/', PermissionsAdminDetailAPIView.as_view(), name='permissions-detail'),
    path('endpoints/', EndpointsAdminListAPIView.as_view(), name='endpoints-list'),
    path('endpoints/<int:endpoint_id>/', EndpointsAdminDetailAPIView.as_view(), name='endpoints-detail'),
]
