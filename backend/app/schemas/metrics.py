from pydantic import BaseModel


class MetricSummary(BaseModel):
    total_requests: int
    success_count: int
    failure_count: int
    success_rate: float
    avg_latency_ms: float | None = None
    p95_latency_ms: float | None = None
    avg_tokens: float | None = None
    avg_cost_usd: float | None = None
    cost_per_request_usd: float | None = None


class ModelMetrics(BaseModel):
    model: str
    total_requests: int
    success_rate: float
    avg_latency_ms: float | None = None
    avg_tokens: float | None = None
    avg_cost_usd: float | None = None


class MetricsResponse(BaseModel):
    summary: MetricSummary
    by_model: list[ModelMetrics]
