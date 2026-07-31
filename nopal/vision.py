import re
from dataclasses import dataclass

import cv2
import numpy as np
import pytesseract

from nopal.config import settings
from nopal.schemas import BoundingBox, PlateDetection


@dataclass(slots=True)
class ImageAnalysis:
    width: int
    height: int
    plates: list[PlateDetection]
    warnings: list[str]


def decode_image(data: bytes) -> np.ndarray:
    buffer = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("El archivo enviado no es una imagen compatible")
    return image


def normalize_plate(text: str) -> str | None:
    normalized = re.sub(r"[^A-Z0-9]", "", text.upper())
    return normalized if 4 <= len(normalized) <= 10 else None


def _ocr_plate(crop: np.ndarray) -> tuple[str | None, float]:
    if not settings.enable_ocr:
        return None, 0.0
    if settings.tesseract_command:
        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_command

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    config = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    data = pytesseract.image_to_data(
        threshold,
        config=config,
        output_type=pytesseract.Output.DICT,
    )

    candidates: list[tuple[str, float]] = []
    for text, confidence in zip(data["text"], data["conf"], strict=False):
        plate = normalize_plate(text)
        try:
            score = max(0.0, min(float(confidence) / 100, 1.0))
        except (TypeError, ValueError):
            score = 0.0
        if plate:
            candidates.append((plate, score))
    return max(candidates, key=lambda item: item[1], default=(None, 0.0))


def detect_plates(image: np.ndarray) -> list[PlateDetection]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 11, 17, 17)
    edges = cv2.Canny(filtered, 30, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    detections: list[PlateDetection] = []
    for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:60]:
        perimeter = cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(polygon) != 4:
            continue

        x, y, width, height = cv2.boundingRect(polygon)
        ratio = width / max(height, 1)
        area = width * height
        if not 2.0 <= ratio <= 6.5 or area < 1_500:
            continue

        padding = 4
        crop = image[
            max(0, y - padding) : y + height + padding,
            max(0, x - padding) : x + width + padding,
        ]
        text, confidence = _ocr_plate(crop)
        detections.append(
            PlateDetection(
                text=text,
                confidence=confidence,
                bbox=BoundingBox(x=x, y=y, width=width, height=height),
            )
        )
        if len(detections) >= 5:
            break
    return detections


def analyze_image(data: bytes) -> ImageAnalysis:
    image = decode_image(data)
    height, width = image.shape[:2]
    warnings: list[str] = []
    try:
        plates = detect_plates(image)
    except pytesseract.TesseractNotFoundError:
        plates = []
        warnings.append("Tesseract no está disponible; se omitió el OCR de placas")
    return ImageAnalysis(width=width, height=height, plates=plates, warnings=warnings)
