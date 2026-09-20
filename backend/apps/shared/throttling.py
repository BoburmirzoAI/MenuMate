"""
Rate limiting — DRF throttle klasslari.

Har sinf `scope`ni belgilaydi; chastota `REST_FRAMEWORK.DEFAULT_THROTTLE_RATES`
sozlamasidagi shu scope'ga mos qiymatdan olinadi.

Anonim so'rovlar IP bo'yicha, autentifikatsiya qilinganlar `request.user.pk`
bo'yicha hisoblanadi.

Ishlatilishi:
    from apps.shared.throttling import LoginThrottle

    class LoginAPIView(APIView):
        throttle_classes = [LoginThrottle]
"""
from rest_framework.throttling import SimpleRateThrottle


class _ScopedThrottle(SimpleRateThrottle):
    """SimpleRateThrottle uchun universal wrapper — scope class attribute.

    `ScopedRateThrottle` view'da `throttle_scope` atribut qidiradi, biz esa
    scope'ni subclass'ning o'zida saqlash uchun `SimpleRateThrottle`'ni
    to'g'ridan-to'g'ri kengaytamiz.
    """

    scope: str = ''

    def get_cache_key(self, request, view) -> str:
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {'scope': self.scope, 'ident': ident}


class LoginThrottle(_ScopedThrottle):
    """Login endpoint — brute-force'ga qarshi (daqiqasiga 5 marta)."""
    scope = 'login'


class RegisterThrottle(_ScopedThrottle):
    """Ro'yxatdan o'tish — spam registratsiyalarga qarshi (soatiga 5 marta)."""
    scope = 'register'


class PasswordThrottle(_ScopedThrottle):
    """Parolni tiklash/o'zgartirish — email spam'iga qarshi (soatiga 5 marta)."""
    scope = 'password'


class MenuGenerateThrottle(_ScopedThrottle):
    """Menyu generatsiyasi — og'ir hisoblash (daqiqasiga 5 marta)."""
    scope = 'menu_generate'


class BroadcastThrottle(_ScopedThrottle):
    """Broadcast push (admin) — noto'g'ri spam yuborishga qarshi."""
    scope = 'broadcast'
