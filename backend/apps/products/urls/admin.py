"""Products admin URL'lari."""
from django.urls import path

from apps.products.views.admin import (
    ShoppingListsAdminDetailAPIView,
    ShoppingListsAdminListAPIView,
)

app_name = 'products-admin'

urlpatterns = [
    path('', ShoppingListsAdminListAPIView.as_view(), name='list'),
    path('by-menu/<int:menu_id>/', ShoppingListsAdminDetailAPIView.as_view(), name='by-menu'),
]
