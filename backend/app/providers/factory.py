from fastapi import HTTPException

from app.core.config import settings
from app.providers.base import LLMClient
from app.providers.registry import get_provider_factory, list_providers


def get_llm_client() -> LLMClient:
    provider_name = settings.provider_name.lower()
    factory = get_provider_factory(provider_name)
    if not factory:
        available = ", ".join(list_providers())
        raise HTTPException(
            status_code=500,
            detail=f"Unsupported provider: {settings.provider_name}. Available: {available}",
        )

    try:
        return factory()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
