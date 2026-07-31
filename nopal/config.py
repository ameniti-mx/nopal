from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nopal"
    environment: str = "development"
    max_upload_mb: int = 10
    enable_ocr: bool = True
    tesseract_command: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="NOPAL_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
