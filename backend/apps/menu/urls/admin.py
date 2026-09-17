"""Menu admin URL'lari."""
from django.urls import path

from apps.menu.views.admin import MenusAdminDetailAPIView, MenusAdminListAPIView

app_name = 'menu-admin'

urlpatterns = [
    path('', MenusAdminListAPIView.as_view(), name='list'),
    path('<int:menu_id>/', MenusAdminDetailAPIView.as_view(), name='detail'),
]
