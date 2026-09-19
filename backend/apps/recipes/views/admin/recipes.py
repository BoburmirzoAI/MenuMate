"""Admin: Recipes / Ingredients / AllergenTags CRUD API'lari."""
from django.db.models import Q
from rest_framework.views import APIView

from apps.recipes.models.recipes import AllergenTag, Ingredient, Recipe
from apps.recipes.serializers.admin import (
    AllergenTagAdminSerializer,
    AllergenTagWritableSerializer,
    IngredientAdminSerializer,
    IngredientWritableSerializer,
    RecipeAdminDetailSerializer,
    RecipeAdminListSerializer,
    RecipeWritableSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class RecipesAdminListAPIView(APIView):
    """GET/POST /admin/recipes/"""
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
            status_code=200,
        )

    def post(self, request):
        serializer = RecipeWritableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        return CustomResponse.created(
            request=request,
            data=RecipeAdminDetailSerializer(recipe).data,
            status_code=201,
        )


class RecipesAdminDetailAPIView(APIView):
    """GET/PATCH/DELETE /admin/recipes/<id>/"""
    permission_classes = [IsAdminUser]

    def _get(self, recipe_id) -> Recipe:
        recipe = Recipe.objects.filter(id=recipe_id).first()
        if not recipe:
            raise CustomException("RECIPE_NOT_FOUND", status_code=400)
        return recipe

    def get(self, request, recipe_id):
        return CustomResponse.success(
            request=request,
            data=RecipeAdminDetailSerializer(self._get(recipe_id)).data,
            status_code=200,
        )

    def patch(self, request, recipe_id):
        recipe = self._get(recipe_id)
        serializer = RecipeWritableSerializer(recipe, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=RecipeAdminDetailSerializer(recipe).data,
            status_code=200,
        )

    def delete(self, request, recipe_id):
        self._get(recipe_id).delete()
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)


class IngredientsAdminListAPIView(APIView):
    """GET/POST /admin/recipes/ingredients/"""
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
            status_code=200,
        )

    def post(self, request):
        serializer = IngredientWritableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ingredient = serializer.save()
        return CustomResponse.created(
            request=request,
            data=IngredientAdminSerializer(ingredient).data,
            status_code=201,
        )


class IngredientsAdminDetailAPIView(APIView):
    """GET/PATCH/DELETE /admin/recipes/ingredients/<id>/"""
    permission_classes = [IsAdminUser]

    def _get(self, ingredient_id) -> Ingredient:
        ing = Ingredient.objects.filter(id=ingredient_id).first()
        if not ing:
            raise CustomException("NOT_FOUND", status_code=404)
        return ing

    def get(self, request, ingredient_id):
        return CustomResponse.success(
            request=request,
            data=IngredientAdminSerializer(self._get(ingredient_id)).data,
            status_code=200,
        )

    def patch(self, request, ingredient_id):
        ing = self._get(ingredient_id)
        serializer = IngredientWritableSerializer(ing, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=IngredientAdminSerializer(ing).data,
            status_code=200,
        )

    def delete(self, request, ingredient_id):
        ing = self._get(ingredient_id)
        try:
            ing.delete()
        except Exception:
            raise CustomException(
                "VALIDATION_ERROR",
                status_code=400,
                errors={"detail": "Ingredient retseptlarda ishlatilmoqda"},
            )
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)


class AllergenTagsAdminListAPIView(APIView):
    """GET/POST /admin/recipes/allergens/"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = AllergenTag.objects.order_by('name_uz')
        return CustomResponse.success(
            request=request,
            data=AllergenTagAdminSerializer(qs, many=True).data,
            status_code=200,
        )

    def post(self, request):
        serializer = AllergenTagWritableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()
        return CustomResponse.created(
            request=request,
            data=AllergenTagAdminSerializer(tag).data,
            status_code=201,
        )


class AllergenTagsAdminDetailAPIView(APIView):
    """GET/PATCH/DELETE /admin/recipes/allergens/<id>/"""
    permission_classes = [IsAdminUser]

    def _get(self, tag_id) -> AllergenTag:
        tag = AllergenTag.objects.filter(id=tag_id).first()
        if not tag:
            raise CustomException("NOT_FOUND", status_code=404)
        return tag

    def get(self, request, tag_id):
        return CustomResponse.success(
            request=request,
            data=AllergenTagAdminSerializer(self._get(tag_id)).data,
            status_code=200,
        )

    def patch(self, request, tag_id):
        tag = self._get(tag_id)
        serializer = AllergenTagWritableSerializer(tag, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=AllergenTagAdminSerializer(tag).data,
            status_code=200,
        )

    def delete(self, request, tag_id):
        self._get(tag_id).delete()
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)
