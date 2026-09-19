"""
Endpoint-level permission middleware.

Every /api/... request is checked against the Endpoint table:
- access_type='public' → anyone in
- access_type='authenticated' → must have valid JWT
- access_type='permission' → must have the linked Permission's codename
  (via role or direct grant)

Endpoints registered in DB with paths like /api/v1/menu/{id}/products/.
Numeric IDs and UUIDs in the request path are normalized to {id}.
"""
import logging
import re

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger('permissions')


class EndpointPermissionMiddleware(MiddlewareMixin):
    SKIP_PREFIXES = [
        '/admin/',
        '/static/',
        '/media/',
        '/schema/',
        '/api/v1/docs/',
        '/api/v1/redoc/',
        '/api/v1/users/register/',
        '/api/v1/users/login/',
        '/api/v1/users/refresh/',
        '/api/v1/users/forgot-password/',
        '/api/v1/users/reset-password/',
        '/api/v1/devices/version-check/',
    ]

    def process_request(self, request):
        if not request.path.startswith('/api/'):
            return None

        for prefix in self.SKIP_PREFIXES:
            if request.path.startswith(prefix):
                return None

        # Try JWT auth (do not block if missing — Endpoint may be public)
        jwt_authenticator = JWTAuthentication()
        try:
            auth_result = jwt_authenticator.authenticate(request)
            if auth_result is not None:
                request.user, request.auth = auth_result
        except Exception as e:
            logger.debug(f"JWT auth failed: {e}")

        # Lazy import to avoid AppRegistryNotReady at Django startup
        from apps.permissions.models.permissions import Endpoint

        normalized_path = self.normalize_path(request.path)

        has_access = Endpoint.check_access(
            user=getattr(request, 'user', None),
            path=normalized_path,
            method=request.method,
        )

        if has_access:
            return None

        endpoint = Endpoint.objects.filter(
            path=normalized_path,
            method=request.method.upper(),
            is_active=True,
        ).first()

        # Endpoint jadvalida yo'q bo'lsa DRF permission_classes'ga topshiramiz.
        if not endpoint:
            return None

        if endpoint.access_type == 'authenticated':
            message_key = 'UNAUTHORIZED'
        elif endpoint.access_type == 'permission':
            message_key = 'PERMISSION_DENIED'
        else:
            message_key = 'PERMISSION_DENIED'

        logger.warning(
            f"Access denied: {getattr(getattr(request, 'user', None), 'email', 'Anonymous')} "
            f"→ {request.method} {request.path}"
        )

        return self._i18n_error_response(request, message_key)

    @staticmethod
    def _i18n_error_response(request, message_key: str):
        """
        DRF Response'ni middleware'da qaytarish oson emas, shuning uchun
        translator'ni to'g'ridan-to'g'ri chaqirib JsonResponse'da tarjima
        qilingan message qaytaramiz. Format CustomResponse bilan bir xil.
        """
        from apps.shared.exceptions.translator import get_message_detail
        accept_lang = (request.META.get('HTTP_ACCEPT_LANGUAGE', 'uz')
                       .split(',')[0].split(';')[0].split('-')[0].strip().lower())
        detail = get_message_detail(message_key=message_key, lang=accept_lang)
        return JsonResponse(
            {
                'success': False,
                'id': detail['id'],
                'message': detail['message'],
            },
            status=detail['status_code'],
        )

    @staticmethod
    def normalize_path(path):
        """Replace numeric/UUID segments with {id}."""
        STATIC_SEGMENTS = {'api', 'v1', 'v2'}
        parts = path.split('/')
        out = []
        for part in parts:
            if not part or part in STATIC_SEGMENTS:
                out.append(part)
            elif part.isdigit() or re.match(r'^[0-9a-f-]{32,}$', part):
                out.append('{id}')
            else:
                out.append(part)
        return '/'.join(out)
