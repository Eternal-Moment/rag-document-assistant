"""Exception handlers that turn every error into {"error": {"code", "message"}}."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.schemas import ErrorDetail, ErrorResponse
from app.constants import ERROR_HTTP, ERROR_INTERNAL, ERROR_NOT_FOUND, ERROR_VALIDATION

logger = logging.getLogger(__name__)


def error_response(status_code: int, code: str, message: str) -> JSONResponse:
    body = ErrorResponse(error=ErrorDetail(code=code, message=message))
    return JSONResponse(status_code=status_code, content=body.model_dump())


async def _http_exception(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    code = ERROR_NOT_FOUND if exc.status_code == status.HTTP_404_NOT_FOUND else ERROR_HTTP
    return error_response(exc.status_code, code, str(exc.detail))


async def _validation_exception(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    first = exc.errors()[0] if exc.errors() else {}
    location = ".".join(str(part) for part in first.get("loc", ()))
    message = (
        f"{location}: {first.get('msg', 'invalid request')}" if location else "invalid request"
    )
    return error_response(status.HTTP_422_UNPROCESSABLE_CONTENT, ERROR_VALIDATION, message)


async def _unhandled_exception(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error", exc_info=exc)
    return error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, ERROR_INTERNAL, "Internal server error"
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, _http_exception)
    app.add_exception_handler(RequestValidationError, _validation_exception)
    app.add_exception_handler(Exception, _unhandled_exception)
