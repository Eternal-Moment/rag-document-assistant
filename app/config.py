"""Application settings, read once from the environment / .env file."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="RAG Document Assistant", description="Shown in OpenAPI docs")
    database_url: str = Field(
        default="postgresql+psycopg://rag:rag@localhost:5432/rag",
        description="SQLAlchemy URL for Postgres (pgvector)",
    )
    db_connect_timeout_s: int = Field(default=3, ge=1, le=30, description="DB connect timeout")


@lru_cache
def get_settings() -> Settings:
    return Settings()
