from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class PlateDetection(BaseModel):
    text: str | None = None
    confidence: float = Field(ge=0, le=1)
    bbox: BoundingBox


class ObjectDetection(BaseModel):
    label: Literal["person", "vehicle", "motorcycle", "bicycle", "unknown"]
    confidence: float = Field(ge=0, le=1)
    bbox: BoundingBox


class AnalysisResponse(BaseModel):
    request_id: str
    processed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    width: int
    height: int
    plates: list[PlateDetection]
    objects: list[ObjectDetection]
    warnings: list[str] = []
