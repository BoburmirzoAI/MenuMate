"""Users admin URL'lari — `/api/v1/admin/users/*`."""
from django.urls import path

from apps.users.views.admin import (
    UsersAdminDetailAPIView,
    UsersAdminListAPIView,
    UsersAdminPasswordAPIView,
)

app_name = 'users-admin'

urlpatterns = [
    path('', UsersAdminListAPIView.as_view(), name='list'),
    path('<int:user_id>/', UsersAdminDetailAPIView.as_view(), name='detail'),
    path('<int:user_id>/set-password/', UsersAdminPasswordAPIView.as_view(), name='set-password'),
]
