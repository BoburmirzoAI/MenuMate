"""
DRF class-based exception handler.

Xatolarni ko'rib chiqadi va CustomResponse orqali standardlashgan javob
qaytaradi. `apps.shared.messages`dan tarjimalar ham ushbu handler orqali
foydalanuvchi tiliga moslanadi.
"""
import logging
import traceback
from typing import Any, Dict, Optional

from django.http import Http404
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAcceptable,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    Throttled,
    UnsupportedMediaType,
    ValidationError,
)
from rest_framework.response import Response

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.utils.custom_response import CustomResponse

logger = logging.getLogger(__name__)


class DRFExceptionHandler:
    """DRF exception → CustomResponse.error() convertor."""

    EXCEPTION_MAPPING = {
        ValidationError: "VALIDATION_ERROR",
        Http404: "NOT_FOUND",
        NotFound: "NOT_FOUND",
        PermissionDenied: "PERMISSION_DENIED",
        NotAuthenticated: "UNAUTHORIZED",
        AuthenticationFailed: "AUTHENTICATION_FAILED",
        MethodNotAllowed: "METHOD_NOT_ALLOWED",
        NotAcceptable: "NOT_ACCEPTABLE",
        UnsupportedMediaType: "UNSUPPORTED_MEDIA_TYPE",
        Throttled: "THROTTLED",
    }

    def handle_exception(self, exc, context):
        request = context.get("request")

        # --- 1. CustomException ---
        if isinstance(exc, CustomException):
            return CustomResponse.error(
                message_key=exc.message_key,
                request=request,
                context=exc.context,
                errors=exc.errors,
                status_code=exc.status_code,
            )

        # --- 2. DRF ValidationError — struktura saqlanadi ---
        if isinstance(exc, ValidationError):
            return CustomResponse.error(
                message_key="VALIDATION_ERROR",
                request=request,
                errors=exc.detail,  # dict/list — field errors saqlanadi
            )

        # --- 3. Boshqa known DRF exception'lar ---
        for exc_type, message_key in self.EXCEPTION_MAPPING.items():
            if isinstance(exc, exc_type):
                return CustomResponse.error(
                    message_key=message_key,
                    request=request,
                    errors=self._get_error_detail(exc),
                )

        # --- 4. Unmapped APIException (masalan custom DRF exception'lar) ---
        if isinstance(exc, APIException):
            return CustomResponse.error(
                message_key="UNKNOWN_ERROR",
                request=request,
                errors=self._get_error_detail(exc),
                status_code=exc.status_code,
            )

        # --- 5. Kutilmagan (Python) exception ---
        logger.exception("Unhandled exception: %s", exc)
        logger.debug(traceback.format_exc())

        return CustomResponse.error(
            message_key="UNKNOWN_ERROR",
            request=request,
        )

    @staticmethod
    def _get_error_detail(exc):
        """DRF exception'dan struktura ko'rinishida detail olish."""
        detail = getattr(exc, 'detail', None)
        if detail is not None:
            return detail
        return str(exc)


exception_handler_instance = DRFExceptionHandler()


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[Response]:
    return exception_handler_instance.handle_exception(exc, context)
