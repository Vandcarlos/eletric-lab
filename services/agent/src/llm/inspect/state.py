from typing import Any, TypedDict


class InspectState(TypedDict, total=False):
    message: str
    attachments: list[dict[str, Any]]
    response: str
    image_url: str | None
    inspection_status: str
