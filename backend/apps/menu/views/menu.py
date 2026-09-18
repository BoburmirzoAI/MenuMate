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
        raise CustomException("FAMILY_NOT_FOUND")
    return family


def _get_user_menu(user, menu_id: int) -> Menu:
    menu = Menu.objects.filter(id=menu_id, family__user=user).first()
    if not menu:
        raise CustomException("MENU_NOT_FOUND")
    return menu


def _get_user_meal(user, meal_id: int) -> MenuMeal:
    meal = MenuMeal.objects.filter(
        id=meal_id, day__menu__family__user=user,
    ).select_related('day__menu').first()
    if not meal:
        raise CustomException("MEAL_NOT_FOUND")
    return meal


class MenuListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        # POST (menyu yaratish) — og'ir hisoblash, alohida limit.
        # GET (ro'yxat) — oddiy default user throttle bilan ketadi.
        if self.request.method == 'POST':
            return [MenuGenerateThrottle()]
        return super().get_throttles()

    def get(self, request):
        family = _get_family(request.user)
        qs = Menu.objects.filter(family=family)
        return CustomResponse.success(
            request=request,
            data=MenuListSerializer(qs, many=True).data,
        )

    def post(self, request):
        family = _get_family(request.user)
        if not family.members.exists():
            raise CustomException("FAMILY_HAS_NO_MEMBERS")

        serializer = CreateMenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_date = serializer.validated_data['start_date']
        duration = serializer.validated_data['duration']

        # Foydalanuvchi menyuni "almashtirmoqda" — shu start_date ga menyu bo'lsa,
        # eskini o'chirib yangisini yaratamiz. Aks holda ikkita menyu bir vaqtda
        # qolib, list.first ordering shubhali bo'lardi.
        Menu.objects.filter(family=family, start_date=start_date).delete()

        menu = create_empty_menu(
            family=family, start_date=start_date, duration=duration,
        )
        return CustomResponse.created(
            request=request,
            message_key="MENU_CREATED",
            data=MenuDetailSerializer(menu).data,
        )


class MenuDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        return CustomResponse.success(
            request=request,
            data=MenuDetailSerializer(menu).data,
        )

    def delete(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        menu.delete()
        return CustomResponse.success(request=request, message_key="DELETED")


class MenuClearAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        clear_menu(menu)
        return CustomResponse.success(
            request=request,
            message_key="MENU_CLEARED",
            data=MenuDetailSerializer(menu).data,
        )


class MenuStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        return CustomResponse.success(request=request, data=menu_stats(menu))


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
                errors={"category": f"kerak: {sorted(valid)}"},
            )

        recipes = recommend_recipes(meal.day.menu.family, meal, category)[:50]
        return CustomResponse.success(
            request=request,
            data=RecipeShortSerializer(recipes, many=True).data,
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
            raise CustomException("RECIPE_NOT_FOUND")

        item, _ = MenuMealItem.objects.update_or_create(
            meal=meal, category=category, defaults={'recipe': recipe},
        )
        return CustomResponse.created(
            request=request,
            message_key="MEAL_ITEM_ADDED",
            data=MenuMealItemSerializer(item).data,
        )


class MealItemDetailAPIView(APIView):
    """DELETE /menus/meals/<meal_id>/items/<item_id>/"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, meal_id, item_id):
        meal = _get_user_meal(request.user, meal_id)
        item = MenuMealItem.objects.filter(id=item_id, meal=meal).first()
        if not item:
            raise CustomException("MEAL_ITEM_NOT_FOUND")
        item.delete()
        return CustomResponse.success(request=request, message_key="DELETED")
