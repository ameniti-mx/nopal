FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md ./
COPY nopal ./nopal
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD ["uvicorn", "nopal.main:app", "--host", "0.0.0.0", "--port", "8000"]
