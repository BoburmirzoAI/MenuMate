"""Admin panel API'lari uchun ruxsat sinfi."""
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Faqat admin (superuser yoki `is_staff=True`) foydalanuvchi kira olsin.

    Django'ning o'z `IsAdminUser`iga o'xshash, lekin `is_superuser`ni ham qabul
    qiladi. Har `/api/v1/admin/*` endpoint shu permission bilan boshlanadi.
    """

    message = "Admin panel uchun ruxsat kerak"

    def has_permission(self, request, view) -> bool:
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return bool(user.is_staff or user.is_superuser)
