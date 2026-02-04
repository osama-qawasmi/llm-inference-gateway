from abc import ABC, abstractmethod

from app.schemas.chat import ChatRequest, ChatResponse


class LLMClient(ABC):
    provider_name: str

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        raise NotImplementedError
