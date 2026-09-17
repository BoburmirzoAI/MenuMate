"""Recipes admin URL'lari."""
from django.urls import path

from apps.recipes.views.admin import (
    AllergenTagsAdminDetailAPIView,
    AllergenTagsAdminListAPIView,
    IngredientsAdminDetailAPIView,
    IngredientsAdminListAPIView,
    RecipesAdminDetailAPIView,
    RecipesAdminListAPIView,
)

app_name = 'recipes-admin'

urlpatterns = [
    # Recipes
    path('', RecipesAdminListAPIView.as_view(), name='list'),
    path('<int:recipe_id>/', RecipesAdminDetailAPIView.as_view(), name='detail'),
    # Ingredients
    path('ingredients/', IngredientsAdminListAPIView.as_view(), name='ingredients-list'),
    path(
        'ingredients/<int:ingredient_id>/',
        IngredientsAdminDetailAPIView.as_view(),
        name='ingredients-detail',
    ),
    # Allergen tags
    path('allergens/', AllergenTagsAdminListAPIView.as_view(), name='allergens-list'),
    path(
        'allergens/<int:tag_id>/',
        AllergenTagsAdminDetailAPIView.as_view(),
        name='allergens-detail',
    ),
]
