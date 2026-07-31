# Nopal 🌵

**Open-source computer vision for physical spaces.**

Nopal converts images and camera streams into structured events for access control, mobility, security and property-management systems. It is privacy-first, API-first and designed to run locally at the edge.

## First release

Version `0.1.0` provides:

- FastAPI service with interactive OpenAPI documentation.
- JPEG, PNG and WebP image ingestion.
- License-plate candidate detection using OpenCV.
- Local OCR using Tesseract.
- Structured JSON results with bounding boxes and confidence.
- Upload validation, configurable limits and graceful OCR degradation.
- Docker image and starter API tests.

This is an early baseline, not a production-grade ALPR system. Recognition accuracy depends heavily on camera angle, lighting, motion blur and plate format. Future releases will add trained detectors, RTSP/ONVIF ingestion, event persistence and object tracking.

## Run with Docker

```bash
docker build -t nopal .
docker run --rm -p 8000:8000 nopal
```

Open `http://localhost:8000/docs`.

## Run locally

Python 3.11 and Tesseract are required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn nopal.main:app --reload
```

## Analyze an image

```bash
curl -X POST http://localhost:8000/v1/analyze/image \
  -F 'image=@vehicle.jpg'
```

Example response:

```json
{
  "request_id": "aa1f43e8-d193-45b0-a5c9-fdd60504f273",
  "processed_at": "2026-07-31T15:00:00Z",
  "width": 1920,
  "height": 1080,
  "plates": [
    {
      "text": "ABC123A",
      "confidence": 0.87,
      "bbox": {"x": 811, "y": 624, "width": 230, "height": 64}
    }
  ],
  "objects": [],
  "warnings": []
}
```

## Configuration

Environment variables use the `NOPAL_` prefix:

| Variable | Default | Description |
| --- | --- | --- |
| `NOPAL_MAX_UPLOAD_MB` | `10` | Maximum image size. |
| `NOPAL_ENABLE_OCR` | `true` | Enables plate OCR. |
| `NOPAL_TESSERACT_COMMAND` | empty | Custom Tesseract executable path. |

## Roadmap

- Trained license-plate detector for Mexican formats.
- Vehicle, person, motorcycle and bicycle detection.
- RTSP and ONVIF camera connectors.
- Entry/exit events and multi-camera tracking.
- Privacy masks and configurable retention.
- Webhooks, Open Condo and Ameniti integrations.
- Edge deployment profiles for CPU, CUDA and embedded devices.

## Principles

1. Local processing first.
2. Open formats and interoperable APIs.
3. Privacy by design.
4. Human review for consequential decisions.
5. No facial identification in the core project.

## License

Apache License 2.0.
