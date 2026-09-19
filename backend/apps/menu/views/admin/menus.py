"""Admin: barcha foydalanuvchilarning menyulari."""
from rest_framework.views import APIView

from apps.menu.models.menu import Menu
from apps.menu.serializers.admin import (
    MenuAdminDetailSerializer,
    MenuAdminListSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class MenusAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Menu.objects.select_related('family', 'family__user').order_by('-created_at')

        status = request.query_params.get('status')
        if status in ('ACTIVE', 'COMPLETED'):
            qs = qs.filter(status=status)

        return CustomResponse.success(
            request=request,
            data=MenuAdminListSerializer(qs, many=True).data,
            status_code=200,
        )


class MenusAdminDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, menu_id):
        menu = Menu.objects.filter(id=menu_id).first()
        if not menu:
            raise CustomException("MENU_NOT_FOUND", status_code=404)
        return CustomResponse.success(
            request=request,
            data=MenuAdminDetailSerializer(menu).data,
            status_code=200,
        )

    def delete(self, request, menu_id):
        menu = Menu.objects.filter(id=menu_id).first()
        if not menu:
            raise CustomException("MENU_NOT_FOUND", status_code=404)
        menu.delete()
        return CustomResponse.success(request=request, message_key="DELETED", status_code=200)
