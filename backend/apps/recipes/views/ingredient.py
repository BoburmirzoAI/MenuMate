"""Ingredient va AllergenTag view'lari — read-only reference data."""
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.recipes.models.recipes import AllergenTag, Ingredient
from apps.recipes.serializers.allergen import (
    AllergenTagSerializer,
    IngredientSerializer,
)
from apps.shared.utils.custom_response import CustomResponse


class AllergenTagListAPIView(ListAPIView):
    """GET /recipes/allergens/"""
    permission_classes = [IsAuthenticated]
    serializer_class = AllergenTagSerializer
    queryset = AllergenTag.objects.all()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return CustomResponse.success(request=request, data=serializer.data, status_code=200)


class IngredientListAPIView(ListAPIView):
    """
    GET /recipes/ingredients/
      ?category=VEGETABLE — kategoriya bo'yicha
      ?search=piyoz       — nom bo'yicha qidiruv
    """
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.prefetch_related('allergen_tags').all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        category = request.query_params.get('category')
        if category:
            qs = qs.filter(category=category.upper())

        search = request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_uz__icontains=search)
                | Q(name_ru__icontains=search)
                | Q(name_en__icontains=search)
            )

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return CustomResponse.success(
                request=request,
                data=self.paginator.get_paginated_data(serializer.data),
                status_code=200,
            )

        serializer = self.get_serializer(qs, many=True)
        return CustomResponse.success(request=request, data=serializer.data, status_code=200)
