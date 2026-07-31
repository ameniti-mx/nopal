# Nopal 🌵

**Visión computacional de código abierto para espacios físicos.**

Nopal convierte imágenes y transmisiones de cámaras en eventos estructurados para sistemas de control de acceso, movilidad, seguridad y administración de inmuebles. Está diseñado con privacidad desde el origen, una arquitectura centrada en API y la capacidad de ejecutarse localmente en el borde.

## Primera versión

La versión `0.1.0` incluye:

- Servicio desarrollado con FastAPI y documentación interactiva OpenAPI.
- Recepción de imágenes JPEG, PNG y WebP.
- Detección de candidatos a placa mediante OpenCV.
- Reconocimiento óptico de caracteres local con Tesseract.
- Resultados JSON estructurados con coordenadas y nivel de confianza.
- Validación de archivos, límites configurables y degradación controlada cuando el OCR no está disponible.
- Imagen de Docker y pruebas iniciales de la API.

Esta es una base temprana y todavía no constituye un sistema ALPR listo para producción. La precisión depende significativamente del ángulo de la cámara, la iluminación, el desenfoque por movimiento y el formato de la placa. Las siguientes versiones incorporarán detectores entrenados, conexión con cámaras RTSP/ONVIF, persistencia de eventos y seguimiento de objetos.

## Ejecutar con Docker

```bash
docker build -t nopal .
docker run --rm -p 8000:8000 nopal
```

Abre `http://localhost:8000/docs` para consultar y probar la API.

## Ejecutar localmente

Se requiere Python 3.11 y Tesseract.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn nopal.main:app --reload
```

## Analizar una imagen

```bash
curl -X POST http://localhost:8000/v1/analyze/image \
  -F 'image=@vehiculo.jpg'
```

Respuesta de ejemplo:

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

Los nombres de los campos se conservan en inglés para mantener una API estable e interoperable.

## Configuración

Las variables de entorno utilizan el prefijo `NOPAL_`:

| Variable | Valor predeterminado | Descripción |
| --- | --- | --- |
| `NOPAL_MAX_UPLOAD_MB` | `10` | Tamaño máximo permitido para una imagen. |
| `NOPAL_ENABLE_OCR` | `true` | Activa el reconocimiento de caracteres de las placas. |
| `NOPAL_TESSERACT_COMMAND` | vacío | Ruta personalizada al ejecutable de Tesseract. |

## Hoja de ruta

- Detector de placas entrenado para formatos mexicanos.
- Detección de vehículos, personas, motocicletas y bicicletas.
- Conectores para cámaras RTSP y ONVIF.
- Eventos de entrada y salida, y seguimiento entre múltiples cámaras.
- Máscaras de privacidad y políticas configurables de retención.
- Webhooks e integraciones con Open Condo y Ameniti.
- Perfiles de despliegue en el borde para CPU, CUDA y dispositivos integrados.

## Principios

1. Procesamiento local como primera opción.
2. Formatos abiertos y API interoperables.
3. Privacidad desde el diseño.
4. Revisión humana para decisiones con consecuencias relevantes.
5. Sin identificación facial en el núcleo del proyecto.

## Licencia

Apache License 2.0.
