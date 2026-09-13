import logging
from typing import Dict

from .family import FAMILY_MESSAGES
from .menu import MENU_MESSAGES
from .notifications import NOTIFICATIONS_MESSAGES
from .products import PRODUCTS_MESSAGES
from .shared import SHARED_MESSAGES
from .types import MessageTemplate
from .users import USER_MESSAGES

logger = logging.getLogger(__name__)

MESSAGES: Dict[str, MessageTemplate] = {
    **SHARED_MESSAGES,
    **USER_MESSAGES,
    **FAMILY_MESSAGES,
    **MENU_MESSAGES,
    **PRODUCTS_MESSAGES,
    **NOTIFICATIONS_MESSAGES,
}


def _validate_messages():
    all_keys = []
    sources = [
        ("SHARED_MESSAGES", SHARED_MESSAGES),
        ("USER_MESSAGES", USER_MESSAGES),
        ("FAMILY_MESSAGES", FAMILY_MESSAGES),
        ("MENU_MESSAGES", MENU_MESSAGES),
        ("PRODUCTS_MESSAGES", PRODUCTS_MESSAGES),
        ("NOTIFICATIONS_MESSAGES", NOTIFICATIONS_MESSAGES),
    ]

    duplicates = []
    for source_name, messages in sources:
        for key in messages.keys():
            if key in all_keys:
                duplicates.append(f"{key} (found in {source_name})")
            all_keys.append(key)

    if duplicates:
        logger.error(f"Duplicate message keys: {', '.join(duplicates)}")


_validate_messages()


__all__ = [
    'MESSAGES',
    'MessageTemplate',
    'SHARED_MESSAGES',
    'USER_MESSAGES',
    'FAMILY_MESSAGES',
    'MENU_MESSAGES',
]
