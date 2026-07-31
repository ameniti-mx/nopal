# Contribuir a Nopal

Gracias por contribuir a Nopal. Todo cambio debe enviarse mediante un pull request y superar la validación automatizada antes de fusionarse.

## Preparación local

Se requiere Python 3.11 o posterior y Tesseract OCR.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Validaciones obligatorias

Antes de abrir un pull request, ejecuta:

```bash
ruff format --check .
ruff check .
python -m compileall -q nopal tests
pytest --cov=nopal --cov-report=term-missing --cov-fail-under=50
docker build -t nopal:local .
```

GitHub Actions repetirá estas validaciones y también ejecutará:

- Pruebas en Python 3.11 y 3.12.
- Auditoría de dependencias con `pip-audit`.
- Análisis estático de seguridad con `bandit`.
- Construcción del paquete Python.
- Construcción de la imagen Docker.

## Reglas para cambios

1. Mantén los pull requests pequeños y enfocados.
2. Incluye pruebas para toda corrección o funcionalidad nueva.
3. No subas secretos, credenciales, placas reales ni imágenes con datos personales.
4. Documenta cambios en endpoints, configuración y comportamiento observable.
5. No incorpores identificación facial al núcleo de Nopal.
6. Ninguna detección debe utilizarse como única base para decisiones sensibles sin revisión humana.

## Convención de commits

Usa mensajes claros y breves, por ejemplo:

- `feat: detectar motocicletas`
- `fix: normalizar placas con guiones`
- `docs: explicar configuración RTSP`
- `ci: actualizar validación de seguridad`

## Protección de la rama principal

Una vez fusionado el workflow de validación, configura una regla de protección para `main` y marca como obligatorio el check **Validación obligatoria**. También se recomienda exigir pull request, impedir pushes directos y descartar aprobaciones cuando haya nuevos commits.
