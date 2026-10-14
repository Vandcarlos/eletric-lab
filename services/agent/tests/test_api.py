from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_old_inspection_endpoint_removed():
    response = client.post("/v1/inspections")
    assert response.status_code == 404
