from fastapi.testclient import TestClient

from nopal.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rejects_unsupported_media_type() -> None:
    response = client.post(
        "/v1/analyze/image",
        files={"image": ("note.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415


def test_rejects_empty_image() -> None:
    response = client.post(
        "/v1/analyze/image",
        files={"image": ("empty.jpg", b"", "image/jpeg")},
    )
    assert response.status_code == 400
