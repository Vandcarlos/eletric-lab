from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_invalid_format():
    response = client.post(
        "/v1/inspections",
        files={"image": ("test.png", b"not-a-png", "image/png")},
    )
    assert response.status_code == 415


def test_demo_report():
    response = client.post(
        "/v1/inspections",
        files={"image": ("test.png", b"\x89PNG\r\n\x1a\nmock", "image/png")},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "needs_review"
