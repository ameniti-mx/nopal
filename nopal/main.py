from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile, status

from nopal import __version__
from nopal.config import settings
from nopal.schemas import AnalysisResponse
from nopal.vision import analyze_image

app = FastAPI(
    title="Nopal Vision API",
    version=__version__,
    description="Open-source, privacy-first computer vision for physical spaces.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "version": __version__}


@app.post("/v1/analyze/image", response_model=AnalysisResponse)
async def analyze_uploaded_image(image: UploadFile = File(...)) -> AnalysisResponse:
    if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Supported formats: JPEG, PNG and WebP",
        )

    payload = await image.read()
    if not payload:
        raise HTTPException(status_code=400, detail="The uploaded image is empty")
    if len(payload) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="The uploaded image is too large")

    try:
        result = analyze_image(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return AnalysisResponse(
        request_id=str(uuid4()),
        width=result.width,
        height=result.height,
        plates=result.plates,
        objects=[],
        warnings=result.warnings,
    )
