from pydantic import BaseModel


class UsageRecord(BaseModel):
    id: str
    created_at: str
    provider: str
    model: str
    success: bool
    latency_ms: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cost_usd: float | None = None
    error_message: str | None = None
    message: str
    response: str


class UsageListResponse(BaseModel):
    items: list[UsageRecord]
