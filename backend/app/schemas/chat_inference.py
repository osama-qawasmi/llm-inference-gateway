from pydantic import BaseModel, Field


class ChatInferenceRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    model: str | None = None


class ChatInferenceResponse(BaseModel):
    reply: str
    model: str
    latency_ms: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cost_usd: float | None = None