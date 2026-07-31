from fastapi.testclient import TestClient

from nopal.main import app
from nopal.vision import normalize_plate

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


def test_rejects_invalid_image_payload() -> None:
    response = client.post(
        "/v1/analyze/image",
        files={"image": ("broken.jpg", b"not-an-image", "image/jpeg")},
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "El archivo enviado no es una imagen compatible"


def test_normalizes_plate_text() -> None:
    assert normalize_plate("abc-123-a") == "ABC123A"
    assert normalize_plate("a!@#") is None
    assert normalize_plate("ABCDEFGHIJK") is None
