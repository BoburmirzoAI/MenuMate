"""Admin: Xarid ro'yxatlari."""
from rest_framework.views import APIView

from apps.products.models.products import ShoppingList
from apps.products.serializers.admin import ShoppingListAdminSerializer
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class ShoppingListsAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = ShoppingList.objects.select_related('menu__family').prefetch_related(
            'items__ingredient',
        ).order_by('-created_at')[:100]
        return CustomResponse.success(
            request=request,
            data=ShoppingListAdminSerializer(qs, many=True).data,
            status_code=200,
        )


class ShoppingListsAdminDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, menu_id):
        sl = ShoppingList.objects.filter(menu_id=menu_id).select_related(
            'menu__family',
        ).prefetch_related('items__ingredient').first()
        if not sl:
            raise CustomException("NOT_FOUND", status_code=404)
        return CustomResponse.success(
            request=request,
            data=ShoppingListAdminSerializer(sl).data,
            status_code=200,
        )
