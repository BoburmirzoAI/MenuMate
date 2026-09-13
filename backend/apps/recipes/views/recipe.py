"""
Recipe views — read-only public API.

Query parametrlari:
  - category (BREAKFAST/LUNCH/DINNER/SOUP/SALAD/DRINK/DESSERT/BREAD/SNACK)
  - season (SUMMER/WINTER/AUTUMN/SPRING/ALL)
  - is_hot (true/false)
  - search (name_uz/ru/en da qidiruv)
  - exclude_allergens (slug ro'yxat: "dairy,gluten")
  - max_prep_time (daqiqada)
  - max_calories
"""
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.recipes.models.recipes import Recipe
from apps.recipes.serializers.recipe import (
    RecipeDetailSerializer,
    RecipeListSerializer,
)
from apps.shared.utils.custom_response import CustomResponse


class RecipeListAPIView(ListAPIView):
    """GET /recipes/ — retseptlar ro'yxati filter bilan."""
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeListSerializer
    queryset = Recipe.objects.prefetch_related('allergen_tags').all()

    def _apply_filters(self, qs, params):
        category = params.get('category')
        if category:
            qs = qs.filter(category=category.upper())

        season = params.get('season')
        if season:
            qs = qs.filter(Q(season=season.upper()) | Q(season='ALL'))

        is_hot = params.get('is_hot')
        if is_hot is not None:
            qs = qs.filter(is_hot=is_hot.lower() in ('true', '1', 'yes'))

        search = params.get('search')
        if search:
            qs = qs.filter(
                Q(name_uz__icontains=search)
                | Q(name_ru__icontains=search)
                | Q(name_en__icontains=search)
            )

        exclude = params.get('exclude_allergens')
        if exclude:
            slugs = [s.strip().lower() for s in exclude.split(',') if s.strip()]
            if slugs:
                qs = qs.exclude(allergen_tags__slug__in=slugs).distinct()

        max_prep = params.get('max_prep_time')
        if max_prep and max_prep.isdigit():
            qs = qs.filter(prep_time_minutes__lte=int(max_prep))

        max_cal = params.get('max_calories')
        if max_cal and max_cal.isdigit():
            qs = qs.filter(calories_per_serving__lte=int(max_cal))

        return qs

    def list(self, request, *args, **kwargs):
        qs = self._apply_filters(self.get_queryset(), request.query_params)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return CustomResponse.success(
                request=request, data=self.paginator.get_paginated_data(serializer.data),
            )

        serializer = self.get_serializer(qs, many=True)
        return CustomResponse.success(request=request, data=serializer.data)


class RecipeDetailAPIView(RetrieveAPIView):
    """GET /recipes/<id>/ — to'liq retsept."""
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.prefetch_related(
        'allergen_tags',
        'ingredients__ingredient',
        'steps',
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return CustomResponse.success(
            request=request,
            data=self.get_serializer(instance).data,
        )
