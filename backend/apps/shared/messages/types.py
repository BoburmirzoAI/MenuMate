from typing import TypedDict, Dict


class MessageTemplate(TypedDict):
    id: str
    messages: Dict[str, str]
    status_code: int
