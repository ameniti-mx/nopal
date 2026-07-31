from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile, status

from nopal import __version__
from nopal.config import settings
from nopal.schemas import AnalysisResponse
from nopal.vision import analyze_image

app = FastAPI(
    title="API de Visión de Nopal",
    version=__version__,
    description=(
        "Visión computacional de código abierto para espacios físicos, "
        "diseñada con privacidad desde el origen y procesamiento local."
    ),
)


@app.get(
    "/health",
    summary="Consultar el estado del servicio",
    description="Confirma que la API está disponible e informa su versión.",
)
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "version": __version__}


@app.post(
    "/v1/analyze/image",
    response_model=AnalysisResponse,
    summary="Analizar una imagen",
    description=(
        "Recibe una imagen JPEG, PNG o WebP, localiza posibles placas vehiculares "
        "y ejecuta OCR local cuando está habilitado."
    ),
)
async def analyze_uploaded_image(
    image: UploadFile = File(..., description="Imagen que será analizada por Nopal."),
) -> AnalysisResponse:
    if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Formatos compatibles: JPEG, PNG y WebP",
        )

    payload = await image.read()
    if not payload:
        raise HTTPException(status_code=400, detail="La imagen enviada está vacía")
    if len(payload) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="La imagen enviada supera el tamaño permitido")

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
