"""
Rate limiting — DRF throttle klasslari.

`ScopedRateThrottle` orqali har endpoint uchun alohida chastota belgilanadi.
Chastota `REST_FRAMEWORK.DEFAULT_THROTTLE_RATES` sozlamasida (base settings).

Ishlatilishi:
    from apps.shared.throttling import LoginThrottle

    class LoginAPIView(APIView):
        throttle_classes = [LoginThrottle]

Har throttle sinf o'z `scope`ini beradi va DRF Redis/cache orqali
foydalanuvchi (yoki IP) hisobini yuritadi.

Anonim so'rovlar IP bo'yicha, autentifikatsiya qilinganlar `request.user.pk`
bo'yicha hisoblanadi.
"""
from rest_framework.throttling import ScopedRateThrottle


class LoginThrottle(ScopedRateThrottle):
    """Login endpoint — brute-force'ga qarshi (daqiqasiga 5 marta)."""
    scope = 'login'


class RegisterThrottle(ScopedRateThrottle):
    """Ro'yxatdan o'tish — spam registratsiyalarga qarshi (soatiga 5 marta)."""
    scope = 'register'


class PasswordThrottle(ScopedRateThrottle):
    """Parolni tiklash/o'zgartirish — email spam'iga qarshi (soatiga 5 marta)."""
    scope = 'password'


class MenuGenerateThrottle(ScopedRateThrottle):
    """Menyu generatsiyasi — og'ir hisoblash (daqiqasiga 5 marta)."""
    scope = 'menu_generate'


class BroadcastThrottle(ScopedRateThrottle):
    """Broadcast push (admin) — noto'g'ri spam yuborishga qarshi."""
    scope = 'broadcast'
