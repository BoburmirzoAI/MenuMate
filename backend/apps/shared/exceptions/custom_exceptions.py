"""
Custom exception — loyihaning barcha biznes-logika xatolari uchun.

Ishlatilishi:
    raise CustomException("EMAIL_ALREADY_EXISTS")
    raise CustomException("VALIDATION_ERROR", errors={"email": "invalid"})
    raise CustomException("USER_NOT_FOUND", context={"user_id": 42})
    raise CustomException("SOMETHING", status_code=418)
"""
from typing import Any, Dict, Optional, Union


class CustomException(Exception):
    def __init__(
            self,
            message_key: str,
            context: Optional[Dict[str, Any]] = None,
            errors: Union[Dict[str, Any], list, str, None] = None,
            status_code: Optional[int] = None,
    ):
        self.message_key = message_key
        self.context = context or {}
        self.errors = errors
        self.status_code = status_code
        super().__init__(message_key)

    def __str__(self):
        return f"CustomException({self.message_key})"
