from django.urls import path

from apps.menu.views.menu import (
    MealItemDetailAPIView,
    MealItemsAPIView,
    MenuClearAPIView,
    MenuDetailAPIView,
    MenuListCreateAPIView,
    MenuStatsAPIView,
    RecommendationsAPIView,
)
from apps.products.views.products import (
    RegenerateShoppingListAPIView,
    ShoppingListAPIView,
)

app_name = 'menu'

urlpatterns = [
    path('', MenuListCreateAPIView.as_view(), name='list-create'),
    path('<int:menu_id>/', MenuDetailAPIView.as_view(), name='detail'),
    path('<int:menu_id>/clear/', MenuClearAPIView.as_view(), name='clear'),
    path('<int:menu_id>/stats/', MenuStatsAPIView.as_view(), name='stats'),

    path('meals/<int:meal_id>/recommendations/',
         RecommendationsAPIView.as_view(), name='recommendations'),
    path('meals/<int:meal_id>/items/',
         MealItemsAPIView.as_view(), name='meal-items'),
    path('meals/<int:meal_id>/items/<int:item_id>/',
         MealItemDetailAPIView.as_view(), name='meal-item-detail'),

    path('<int:menu_id>/products/',
         ShoppingListAPIView.as_view(), name='shopping-list'),
    path('<int:menu_id>/products/regenerate/',
         RegenerateShoppingListAPIView.as_view(), name='shopping-list-regenerate'),
]
