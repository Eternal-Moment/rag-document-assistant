from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.db.session import get_session
from app.main import create_app


@pytest.fixture
def fake_session() -> MagicMock:
    return MagicMock()


@pytest.fixture
def client(fake_session: MagicMock) -> Iterator[TestClient]:
    """App client with the DB session replaced by a mock (no Postgres needed)."""
    app = create_app()
    app.dependency_overrides[get_session] = lambda: fake_session
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
