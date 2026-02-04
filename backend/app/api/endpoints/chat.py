from fastapi import APIRouter, Depends

from app.providers.base import LLMClient
from app.providers.factory import get_llm_client
from app.schemas.chat_inference import ChatInferenceRequest, ChatInferenceResponse
from app.services.chat import run_chat_inference

router = APIRouter()


@router.post("/chat", response_model=ChatInferenceResponse)
async def chat(
    payload: ChatInferenceRequest,
    client: LLMClient = Depends(get_llm_client),
) -> ChatInferenceResponse:
    return await run_chat_inference(payload, client)
