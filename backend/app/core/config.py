import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = BACKEND_DIR.parent
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev").lower()
ENV_FILES = (
    BACKEND_DIR / ".env",
    REPO_DIR / ".env",
    BACKEND_DIR / f".env.{ENVIRONMENT}",
    REPO_DIR / f".env.{ENVIRONMENT}",
)


class Settings(BaseSettings):
    app_name: str = "llm-inference-gateway"
    api_v1_prefix: str = "/api/v1"

    provider_name: str = "openai"
    openai_api_key: str = ""
    default_model: str = "gpt-4o-mini"
    openai_model: str | None = None
    openai_base_url: str | None = None
    openai_timeout_seconds: float = 30.0
    model_pricing_json: str | None = None

    db_path: str = "data/app.db"

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        extra="ignore",
    )

    @field_validator("openai_base_url", mode="before")
    @classmethod
    def _empty_string_to_none(cls, value: str | None) -> str | None:
        if isinstance(value, str) and not value.strip():
            return None
        return value


settings = Settings()
