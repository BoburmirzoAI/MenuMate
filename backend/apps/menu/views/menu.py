from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.family.models.family import FamilyProfile
from apps.menu.models.menu import Menu, MenuMeal, MenuMealItem
from apps.menu.serializers.menu import (
    AddMealItemSerializer,
    CreateMenuSerializer,
    MenuDetailSerializer,
    MenuListSerializer,
    MenuMealItemSerializer,
    RecipeShortSerializer,
)
from apps.menu.utils.builder import clear_menu, create_empty_menu
from apps.menu.utils.recommender import recommend_recipes
from apps.menu.utils.stats import menu_stats
from apps.recipes.models.recipes import Recipe
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.throttling import MenuGenerateThrottle
from apps.shared.utils.custom_response import CustomResponse


def _get_family(user) -> FamilyProfile:
    family = FamilyProfile.objects.filter(user=user).first()
    if not family:
        raise CustomException(
            "FAMILY_NOT_FOUND",
            status_code=404,
            errors={
                "detail": f"User user_id={user.pk} has no family profile",
                "user_id": user.pk,
                "reason": "user_has_no_family",
            },
        )
    return family


def _get_user_menu(user, menu_id: int) -> Menu:
    menu = Menu.objects.filter(id=menu_id, family__user=user).first()
    if not menu:
        raise CustomException(
            "MENU_NOT_FOUND",
            status_code=404,
            errors={
                "detail": f"Menu id={menu_id} not found or does not belong to user_id={user.pk}",
                "menu_id": menu_id,
                "user_id": user.pk,
                "reason": "menu_not_found_or_forbidden",
            },
        )
    return menu


def _get_user_meal(user, meal_id: int) -> MenuMeal:
    meal = MenuMeal.objects.filter(
        id=meal_id, day__menu__family__user=user,
    ).select_related('day__menu').first()
    if not meal:
        raise CustomException(
            "MEAL_NOT_FOUND",
            status_code=404,
            errors={
                "detail": f"Meal id={meal_id} not found or does not belong to user_id={user.pk}",
                "meal_id": meal_id,
                "user_id": user.pk,
                "reason": "meal_not_found_or_forbidden",
            },
        )
    return meal


class MenuListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        """POST menyu yaratish og'ir hisoblash — alohida limit; GET default'da qoladi."""
        if self.request.method == 'POST':
            return [MenuGenerateThrottle()]
        return super().get_throttles()

    def get(self, request):
        family = _get_family(request.user)
        qs = Menu.objects.filter(family=family)
        return CustomResponse.success(
            request=request,
            data=MenuListSerializer(qs, many=True).data,
            status_code=200,
        )

    def post(self, request):
        family = _get_family(request.user)
        if not family.members.exists():
            raise CustomException(
                "FAMILY_HAS_NO_MEMBERS",
                status_code=400,
                errors={
                    "detail": f"Family family_id={family.pk} has zero members — cannot build menu",
                    "family_id": family.pk,
                    "user_id": request.user.pk,
                    "member_count": 0,
                    "reason": "family_has_no_members",
                    "action_required": "add_family_members_first",
                },
            )

        serializer = CreateMenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_date = serializer.validated_data['start_date']
        duration = serializer.validated_data['duration']

        # Shu start_date'ga mavjud menyu bo'lsa eskisini o'chiramiz — aks holda
        # ikkita menyu bir vaqtda qolib list ordering shubhali bo'lardi.
        Menu.objects.filter(family=family, start_date=start_date).delete()

        menu = create_empty_menu(
            family=family, start_date=start_date, duration=duration,
        )
        return CustomResponse.created(
            request=request,
            message_key="MENU_CREATED",
            data=MenuDetailSerializer(menu).data,
            status_code=201,
        )


class MenuDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        return CustomResponse.success(
            request=request,
            data=MenuDetailSerializer(menu).data,
            status_code=200,
        )

    def delete(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        menu.delete()
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)


class MenuClearAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        clear_menu(menu)
        return CustomResponse.success(
            request=request,
            message_key="MENU_CLEARED",
            data=MenuDetailSerializer(menu).data,
            status_code=200,
        )


class MenuStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        return CustomResponse.success(request=request, data=menu_stats(menu), status_code=200)


class RecommendationsAPIView(APIView):
    """GET /menus/meals/<meal_id>/recommendations/?category=DRINK"""
    permission_classes = [IsAuthenticated]

    def get(self, request, meal_id):
        meal = _get_user_meal(request.user, meal_id)
        category = request.query_params.get('category')

        valid = {c[0] for c in MenuMealItem.Category.choices}
        if category not in valid:
            raise CustomException(
                "VALIDATION_ERROR",
                status_code=400,
                errors={
                    "detail": f"category='{category}' is not in allowed set: {sorted(valid)}",
                    "field": "category",
                    "value": category,
                    "allowed": sorted(valid),
                    "reason": "invalid_meal_category",
                },
            )

        recipes = recommend_recipes(meal.day.menu.family, meal, category)[:50]
        return CustomResponse.success(
            request=request,
            data=RecipeShortSerializer(recipes, many=True).data,
            status_code=200,
        )


class MealItemsAPIView(APIView):
    """POST /menus/meals/<meal_id>/items/  (add item)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, meal_id):
        meal = _get_user_meal(request.user, meal_id)
        serializer = AddMealItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = serializer.validated_data['category']
        recipe = Recipe.objects.filter(
            id=serializer.validated_data['recipe_id'],
        ).first()
        if not recipe:
            recipe_id = serializer.validated_data['recipe_id']
            raise CustomException(
                "RECIPE_NOT_FOUND",
                status_code=400,
                errors={
                    "detail": f"Recipe id={recipe_id} does not exist",
                    "field": "recipe_id",
                    "recipe_id": recipe_id,
                    "reason": "unknown_recipe_id",
                },
            )

        item, _ = MenuMealItem.objects.update_or_create(
            meal=meal, category=category, defaults={'recipe': recipe},
        )
        return CustomResponse.created(
            request=request,
            message_key="MEAL_ITEM_ADDED",
            data=MenuMealItemSerializer(item).data,
            status_code=201,
        )


class MealItemDetailAPIView(APIView):
    """DELETE /menus/meals/<meal_id>/items/<item_id>/"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, meal_id, item_id):
        meal = _get_user_meal(request.user, meal_id)
        item = MenuMealItem.objects.filter(id=item_id, meal=meal).first()
        if not item:
            raise CustomException(
                "MEAL_ITEM_NOT_FOUND",
                status_code=404,
                errors={
                    "detail": f"Meal item id={item_id} not found in meal_id={meal_id}",
                    "meal_id": meal_id,
                    "item_id": item_id,
                    "user_id": request.user.pk,
                    "reason": "meal_item_not_found_or_forbidden",
                },
            )
        item.delete()
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)
