from apps.recipes.views.admin.images import (
    ImageSearchAPIView,
    ImageUploadAPIView,
)
from apps.recipes.views.admin.recipes import (
    AllergenTagsAdminDetailAPIView,
    AllergenTagsAdminListAPIView,
    IngredientsAdminDetailAPIView,
    IngredientsAdminListAPIView,
    RecipesAdminDetailAPIView,
    RecipesAdminListAPIView,
)

__all__ = [
    'RecipesAdminListAPIView',
    'RecipesAdminDetailAPIView',
    'IngredientsAdminListAPIView',
    'IngredientsAdminDetailAPIView',
    'AllergenTagsAdminListAPIView',
    'AllergenTagsAdminDetailAPIView',
    'ImageSearchAPIView',
    'ImageUploadAPIView',
]
