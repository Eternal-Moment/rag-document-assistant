"""Pydantic request/response models for the HTTP API."""

from pydantic import BaseModel, Field

from app.constants import ComponentStatus


class ErrorDetail(BaseModel):
    code: str = Field(description="Machine-readable error code, e.g. DOCUMENT_NOT_FOUND")
    message: str = Field(description="Human-readable explanation")


class ErrorResponse(BaseModel):
    error: ErrorDetail = Field(description="The single error shape used by every endpoint")


class HealthResponse(BaseModel):
    db: ComponentStatus = Field(description="Postgres connectivity")

    model_config = {"json_schema_extra": {"examples": [{"db": "ok"}]}}
