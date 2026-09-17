"""Admin: Recipes / Ingredients / AllergenTags API'lari."""
from django.db.models import Q
from rest_framework.views import APIView

from apps.recipes.models.recipes import AllergenTag, Ingredient, Recipe
from apps.recipes.serializers.admin import (
    AllergenTagAdminSerializer,
    IngredientAdminSerializer,
    RecipeAdminDetailSerializer,
    RecipeAdminListSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class RecipesAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Recipe.objects.prefetch_related('allergen_tags').order_by('name_uz')

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(name_uz__icontains=search)
                | Q(name_ru__icontains=search)
                | Q(name_en__icontains=search),
            )

        category = request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)

        return CustomResponse.success(
            request=request,
            data=RecipeAdminListSerializer(qs, many=True).data,
        )


class RecipesAdminDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, recipe_id):
        recipe = Recipe.objects.filter(id=recipe_id).first()
        if not recipe:
            raise CustomException("RECIPE_NOT_FOUND")
        return CustomResponse.success(
            request=request,
            data=RecipeAdminDetailSerializer(recipe).data,
        )


class IngredientsAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Ingredient.objects.order_by('category', 'name_uz')
        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(Q(name_uz__icontains=search) | Q(name_en__icontains=search))
        category = request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return CustomResponse.success(
            request=request,
            data=IngredientAdminSerializer(qs, many=True).data,
        )


class AllergenTagsAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = AllergenTag.objects.order_by('name_uz')
        return CustomResponse.success(
            request=request,
            data=AllergenTagAdminSerializer(qs, many=True).data,
        )
