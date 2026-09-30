from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_case() -> None:
    create = client.post("/cases/analyze", json={"text": "Synthetic policy case"})
    assert create.status_code == 202
    body = create.json()
    assert body["status"] == "received"

    get = client.get(f"/cases/{body['case_id']}")
    assert get.status_code == 200
    assert get.json()["case_id"] == body["case_id"]


def test_reject_empty_case() -> None:
    response = client.post("/cases/analyze", json={"text": ""})
    assert response.status_code == 422


def test_missing_case_returns_404() -> None:
    response = client.get("/cases/not-a-real-case")
    assert response.status_code == 404
