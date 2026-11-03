"""One working test as a starting point."""

from fastapi.testclient import TestClient

from pi_fireplace.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
