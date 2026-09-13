from django.urls import path

from apps.recipes.views.ingredient import (
    AllergenTagListAPIView,
    IngredientListAPIView,
)
from apps.recipes.views.recipe import (
    RecipeDetailAPIView,
    RecipeListAPIView,
)

app_name = 'recipes'

urlpatterns = [
    # --- Recipes ---
    path('', RecipeListAPIView.as_view(), name='list'),
    path('<int:pk>/', RecipeDetailAPIView.as_view(), name='detail'),

    # --- Reference ---
    path('allergens/', AllergenTagListAPIView.as_view(), name='allergens'),
    path('ingredients/', IngredientListAPIView.as_view(), name='ingredients'),
]
