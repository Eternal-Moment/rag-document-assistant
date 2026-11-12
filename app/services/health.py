"""Health checks for the service's dependencies."""

import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.constants import STATUS_ERROR, STATUS_OK, ComponentStatus

logger = logging.getLogger(__name__)


def check_database(session: Session) -> ComponentStatus:
    """Return "ok" if Postgres answers a trivial query, otherwise "error"."""
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.warning("Database health check failed", exc_info=True)
        return STATUS_ERROR
    return STATUS_OK
