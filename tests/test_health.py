from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import create_app


def test_health_ok_when_db_answers(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"db": "ok"}


def test_health_503_when_db_down(client: TestClient, fake_session: MagicMock) -> None:
    fake_session.execute.side_effect = OperationalError("SELECT 1", {}, Exception("down"))

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"db": "error"}


@pytest.mark.integration
def test_health_against_real_postgres() -> None:
    with TestClient(create_app()) as real_client:
        response = real_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"db": "ok"}
