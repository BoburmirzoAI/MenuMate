"""Recipes admin URL'lari."""
from django.urls import path

from apps.recipes.views.admin import (
    AllergenTagsAdminDetailAPIView,
    AllergenTagsAdminListAPIView,
    ImageSearchAPIView,
    ImageUploadAPIView,
    IngredientsAdminDetailAPIView,
    IngredientsAdminListAPIView,
    RecipesAdminDetailAPIView,
    RecipesAdminListAPIView,
)

app_name = 'recipes-admin'

urlpatterns = [
    path('', RecipesAdminListAPIView.as_view(), name='list'),
    path('<int:recipe_id>/', RecipesAdminDetailAPIView.as_view(), name='detail'),

    path('search-image/', ImageSearchAPIView.as_view(), name='search-image'),
    path('upload-image/', ImageUploadAPIView.as_view(), name='upload-image'),

    path('ingredients/', IngredientsAdminListAPIView.as_view(), name='ingredients-list'),
    path('ingredients/<int:ingredient_id>/', IngredientsAdminDetailAPIView.as_view(), name='ingredients-detail'),

    path('allergens/', AllergenTagsAdminListAPIView.as_view(), name='allergens-list'),
    path('allergens/<int:tag_id>/', AllergenTagsAdminDetailAPIView.as_view(), name='allergens-detail'),
]
