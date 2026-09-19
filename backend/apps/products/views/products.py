from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.family.models.family import FamilyProfile
from apps.menu.models.menu import Menu
from apps.products.models.products import ShoppingItem
from apps.products.serializers.products import (
    ShoppingItemSerializer,
    ShoppingListSerializer,
)
from apps.products.utils.generator import generate_shopping_list
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.utils.custom_response import CustomResponse


def _get_user_menu(user, menu_id: int) -> Menu:
    family = FamilyProfile.objects.filter(user=user).first()
    if not family:
        raise CustomException("FAMILY_NOT_FOUND", status_code=404)
    menu = Menu.objects.filter(id=menu_id, family=family).first()
    if not menu:
        raise CustomException("MENU_NOT_FOUND", status_code=404)
    return menu


class ShoppingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        shopping_list = generate_shopping_list(menu)
        return CustomResponse.success(
            request=request,
            data=ShoppingListSerializer(shopping_list).data,
            status_code=200,
        )


class RegenerateShoppingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, menu_id):
        menu = _get_user_menu(request.user, menu_id)
        shopping_list = generate_shopping_list(menu)
        return CustomResponse.success(
            request=request,
            message_key="SHOPPING_LIST_REGENERATED",
            data=ShoppingListSerializer(shopping_list).data,
            status_code=200,
        )


class ShoppingItemToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        item = ShoppingItem.objects.filter(
            id=item_id,
            shopping_list__menu__family__user=request.user,
        ).first()
        if not item:
            raise CustomException("SHOPPING_ITEM_NOT_FOUND", status_code=404)

        is_purchased = request.data.get('is_purchased')
        if is_purchased is not None:
            item.is_purchased = bool(is_purchased)
            item.save(update_fields=['is_purchased'])

        return CustomResponse.success(
            request=request,
            data=ShoppingItemSerializer(item).data,
            message_key="UPDATED",
            status_code=200,
        )
