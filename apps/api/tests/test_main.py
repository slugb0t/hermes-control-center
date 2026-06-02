from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_reports_ok():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "hermes-control-center-api"}


def test_status_endpoint_exposes_allowed_roots(monkeypatch):
    monkeypatch.setenv("HERMES_CONTROL_ALLOWED_ROOTS", "/tmp/private:/tmp/shared")
    client = TestClient(create_app())

    response = client.get("/status")

    assert response.status_code == 200
    assert response.json() == {
        "hermes_connected": False,
        "live_updates": "planned",
        "allowed_roots": ["/tmp/private", "/tmp/shared"],
    }
