from pydantic import BaseModel, Field


class InspectionReport(BaseModel):
    inspection_id: str
    status: str = "needs_review"
    summary: str
    observations: list[str] = Field(default_factory=list)
    required_information: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    annotated_image_url: str | None = None
