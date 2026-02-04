import time

from app.core.pricing import estimate_cost_usd
from app.llm.router import resolve_model
from app.providers.base import LLMClient
from app.repositories.usage_repo import insert_usage
from app.schemas.chat import ChatMessage, ChatRequest
from app.schemas.chat_inference import ChatInferenceRequest, ChatInferenceResponse


async def run_chat_inference(
    payload: ChatInferenceRequest,
    client: LLMClient,
) -> ChatInferenceResponse:
    decision = resolve_model(payload.message, payload.model)
    request = ChatRequest(
        messages=[ChatMessage(role="user", content=payload.message)],
        model=decision.model,
    )
    provider_name = getattr(client, "provider_name", "unknown")
    start_time = time.perf_counter()
    try:
        response = await client.chat(request)
        latency_ms = (time.perf_counter() - start_time) * 1000
        usage = response.usage
        cost_usd = estimate_cost_usd(
            response.model,
            usage.input_tokens if usage else None,
            usage.output_tokens if usage else None,
        )

        insert_usage(
            provider=response.provider,
            model=response.model,
            message=payload.message,
            response=response.output,
            success=True,
            latency_ms=latency_ms,
            input_tokens=usage.input_tokens if usage else None,
            output_tokens=usage.output_tokens if usage else None,
            total_tokens=usage.total_tokens if usage else None,
            cost_usd=cost_usd,
            error_message=None,
        )

        return ChatInferenceResponse(
            reply=response.output,
            model=response.model,
            latency_ms=latency_ms,
            input_tokens=usage.input_tokens if usage else None,
            output_tokens=usage.output_tokens if usage else None,
            total_tokens=usage.total_tokens if usage else None,
            cost_usd=cost_usd,
        )
    except Exception as exc:
        latency_ms = (time.perf_counter() - start_time) * 1000
        insert_usage(
            provider=provider_name,
            model=decision.model,
            message=payload.message,
            response="",
            success=False,
            latency_ms=latency_ms,
            input_tokens=None,
            output_tokens=None,
            total_tokens=None,
            cost_usd=None,
            error_message=str(exc),
        )
        raise
