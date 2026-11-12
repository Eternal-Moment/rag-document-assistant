"""FastAPI application factory."""

from fastapi import FastAPI

from app.api import health
from app.api.errors import register_error_handlers
from app.config import get_settings


def create_app() -> FastAPI:
    app = FastAPI(title=get_settings().app_name, version="0.1.0")
    register_error_handlers(app)
    app.include_router(health.router)
    return app


app = create_app()
