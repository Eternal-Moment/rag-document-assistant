"""Shared constants: error codes and status values used across layers."""

from typing import Final, Literal

# Error codes returned in {"error": {"code", "message"}}
ERROR_VALIDATION: Final = "VALIDATION_ERROR"
ERROR_NOT_FOUND: Final = "NOT_FOUND"
ERROR_HTTP: Final = "HTTP_ERROR"
ERROR_INTERNAL: Final = "INTERNAL_ERROR"
ERROR_SERVICE_UNAVAILABLE: Final = "SERVICE_UNAVAILABLE"

# Health check component status
ComponentStatus = Literal["ok", "error"]
STATUS_OK: Final = "ok"
STATUS_ERROR: Final = "error"
