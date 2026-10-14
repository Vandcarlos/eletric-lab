from typing import Any, TypedDict


class MainState(TypedDict, total=False):
    session_id: str
    requested_type: str
    message: str
    attachments: list[dict[str, Any]]
    intent: str
    response: str
    image_url: str | None
