"""
Standardized API response wrapper with automatic i18n message translation.

Format:
    {
        "success": true|false,
        "id": "<MESSAGE_KEY>",
        "message": "<translated>",
        "data": <optional>,
        "errors": <optional>,
    }
"""
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from rest_framework.request import Request
from rest_framework.response import Response

from apps.shared.exceptions.translator import get_message_detail

logger = logging.getLogger(__name__)


ErrorsType = Union[Dict[str, Any], List[Any], str, None]


@dataclass
class ResponseBody:
    message_key: str
    request: Optional[Request] = None
    context: Optional[Dict[str, Any]] = None

    def get_language(self) -> str:
        if self.request and hasattr(self.request, 'headers'):
            accept_lang = self.request.headers.get('Accept-Language', 'uz')
            lang = accept_lang.split(';')[0].split(',')[0].strip().lower()
            return lang
        return 'uz'

    def _detail(self):
        return get_message_detail(
            message_key=self.message_key,
            lang=self.get_language(),
            context=self.context,
        )

    def to_dict(self, **extra) -> Dict[str, Any]:
        d = self._detail()
        return {"id": d["id"], "message": d["message"], **extra}

    def get_status_code(self) -> int:
        return self._detail()["status_code"]


class CustomResponse:
    """Loyihaning standard response'lari."""

    @staticmethod
    def success(
            message_key: str = "SUCCESS",
            request: Request = None,
            data: Any = None,
            context: Optional[Dict[str, Any]] = None,
            status_code: Optional[int] = None,
            **kwargs,
    ) -> Response:
        body_maker = ResponseBody(message_key=message_key, request=request, context=context)
        extra: Dict[str, Any] = {}
        if data is not None:
            extra["data"] = data
        extra.update(kwargs)
        body = body_maker.to_dict(**extra)
        body["success"] = True
        return Response(body, status=status_code or body_maker.get_status_code())

    @staticmethod
    def created(
            message_key: str = "CREATED",
            request: Request = None,
            data: Any = None,
            context: Optional[Dict[str, Any]] = None,
            **kwargs,
    ) -> Response:
        return CustomResponse.success(
            message_key=message_key, request=request, data=data,
            context=context, status_code=201, **kwargs,
        )

    @staticmethod
    def no_content(status_code: int = 204) -> Response:
        return Response(status=status_code)

    @staticmethod
    def error(
            message_key: str,
            request: Request = None,
            context: Optional[Dict[str, Any]] = None,
            errors: ErrorsType = None,
            status_code: Optional[int] = None,
            **kwargs,
    ) -> Response:
        body_maker = ResponseBody(message_key=message_key, request=request, context=context)
        extra: Dict[str, Any] = {}
        if errors is not None:
            extra["errors"] = errors
        extra.update(kwargs)
        body = body_maker.to_dict(**extra)
        body["success"] = False
        final_status = status_code or body_maker.get_status_code()
        logger.warning(
            "Error response: %s (status=%s)", message_key, final_status,
            extra={'errors': errors, 'context': context},
        )
        return Response(body, status=final_status)

    @staticmethod
    def validation_error(
            errors: ErrorsType,
            request: Request = None,
            message_key: str = "VALIDATION_ERROR",
    ) -> Response:
        return CustomResponse.error(
            message_key=message_key, request=request, errors=errors, status_code=400,
        )

    @staticmethod
    def not_found(
            message_key: str = "NOT_FOUND",
            request: Request = None,
            context: Optional[Dict[str, Any]] = None,
    ) -> Response:
        return CustomResponse.error(
            message_key=message_key, request=request, context=context, status_code=404,
        )

    @staticmethod
    def unauthorized(
            message_key: str = "UNAUTHORIZED",
            request: Request = None,
    ) -> Response:
        return CustomResponse.error(
            message_key=message_key, request=request, status_code=401,
        )

    @staticmethod
    def forbidden(
            message_key: str = "PERMISSION_DENIED",
            request: Request = None,
    ) -> Response:
        return CustomResponse.error(
            message_key=message_key, request=request, status_code=403,
        )
