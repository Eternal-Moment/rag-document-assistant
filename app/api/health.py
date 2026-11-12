"""GET /health — dependency status for load balancers and humans."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.schemas import HealthResponse
from app.constants import STATUS_OK
from app.db.session import get_session
from app.services.health import check_database

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Check service dependencies",
    response_model=HealthResponse,
    responses={503: {"model": HealthResponse, "description": "A dependency is unavailable"}},
)
def health(response: Response, session: Annotated[Session, Depends(get_session)]) -> HealthResponse:
    result = HealthResponse(db=check_database(session))
    if result.db != STATUS_OK:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return result
