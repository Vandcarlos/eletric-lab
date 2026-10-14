from enum import StrEnum
from typing import Any, Literal
from pydantic import BaseModel, Field, ConfigDict


class AgentType(StrEnum):
    INSPECTION = "inspection"
    GENERAL = "general"


class Attachment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["image"]
    url: str = Field(min_length=1, max_length=2048)


class AgentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str = Field(min_length=1, max_length=128)
    type: AgentType = AgentType.GENERAL
    message: str = Field(min_length=1, max_length=8000)
    attachments: list[Attachment] = Field(default_factory=list, max_length=5)
    metadata: dict[str, Any] = Field(default_factory=dict)
