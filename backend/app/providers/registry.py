from collections.abc import Callable

from app.providers.base import LLMClient
from app.providers.openai_client import OpenAIClient

ProviderFactory = Callable[[], LLMClient]

_REGISTRY: dict[str, ProviderFactory] = {
    "openai": OpenAIClient,
}


def get_provider_factory(name: str) -> ProviderFactory | None:
    return _REGISTRY.get(name.lower())


def list_providers() -> list[str]:
    return sorted(_REGISTRY.keys())
