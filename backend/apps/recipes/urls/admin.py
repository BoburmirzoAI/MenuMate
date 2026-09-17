"""Recipes admin URL'lari."""
from django.urls import path

from apps.recipes.views.admin import (
    AllergenTagsAdminListAPIView,
    IngredientsAdminListAPIView,
    RecipesAdminDetailAPIView,
    RecipesAdminListAPIView,
)

app_name = 'recipes-admin'

urlpatterns = [
    path('', RecipesAdminListAPIView.as_view(), name='list'),
    path('<int:recipe_id>/', RecipesAdminDetailAPIView.as_view(), name='detail'),
    path('ingredients/', IngredientsAdminListAPIView.as_view(), name='ingredients'),
    path('allergens/', AllergenTagsAdminListAPIView.as_view(), name='allergens'),
]
