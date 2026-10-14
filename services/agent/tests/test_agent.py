from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_inspection_stream():
    with client.stream("POST", "/v1/agent/stream", json={
        "session_id": "test-session",
        "type": "inspection",
        "message": "Analise o quadro",
    }) as response:
        body = "".join(response.iter_text())
    assert response.status_code == 200
    assert "event: agent.started" in body
    assert "event: message.delta" in body
    assert "event: agent.completed" in body
    assert "event: image.generated" not in body


def test_unknown_type_rejected():
    response = client.post("/v1/agent/stream", json={
        "session_id": "test",
        "type": "unknown",
        "message": "Oi",
    })
    assert response.status_code == 422
