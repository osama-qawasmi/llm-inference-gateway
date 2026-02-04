from openai import AsyncOpenAI

from app.core.config import settings
from app.providers.base import LLMClient
from app.schemas.chat import ChatRequest, ChatResponse


class OpenAIClient(LLMClient):
    provider_name = "openai"

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is not configured.")

        client_kwargs: dict[str, object] = {
            "api_key": settings.openai_api_key,
            "timeout": settings.openai_timeout_seconds,
        }
        if settings.openai_base_url:
            client_kwargs["base_url"] = settings.openai_base_url
        self._client = AsyncOpenAI(**client_kwargs)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        model = request.model or settings.openai_model or settings.default_model
        response = await self._client.chat.completions.create(
            model=model,
            messages=[message.model_dump() for message in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        usage = response.usage
        content = response.choices[0].message.content or ""
        return ChatResponse(
            provider=self.provider_name,
            model=response.model,
            output=content,
            usage=(
                None
                if not usage
                else {
                    "input_tokens": usage.prompt_tokens,
                    "output_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                }
            ),
        )
