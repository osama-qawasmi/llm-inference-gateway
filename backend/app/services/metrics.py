from app.repositories.metrics_repo import (
    get_latency_values,
    get_model_rows,
    get_summary_row,
)
from app.schemas.metrics import MetricSummary, MetricsResponse, ModelMetrics


def _percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    if percentile <= 0:
        return values[0]
    if percentile >= 100:
        return values[-1]
    index = int(round((percentile / 100) * (len(values) - 1)))
    return values[index]


def get_metrics() -> MetricsResponse:
    summary_row = get_summary_row()
    total_requests = int(summary_row.get("total_requests") or 0)
    success_count = int(summary_row.get("success_count") or 0)
    failure_count = int(summary_row.get("failure_count") or 0)
    success_rate = (success_count / total_requests) if total_requests else 0.0

    latencies = get_latency_values()
    p95_latency = _percentile(latencies, 95)

    total_cost = summary_row.get("total_cost_usd")
    cost_per_request = (
        (total_cost / total_requests) if total_requests and total_cost else None
    )

    summary = MetricSummary(
        total_requests=total_requests,
        success_count=success_count,
        failure_count=failure_count,
        success_rate=round(success_rate, 4),
        avg_latency_ms=summary_row.get("avg_latency_ms"),
        p95_latency_ms=p95_latency,
        avg_tokens=summary_row.get("avg_tokens"),
        avg_cost_usd=summary_row.get("avg_cost_usd"),
        cost_per_request_usd=cost_per_request,
    )

    by_model = []
    for row in get_model_rows():
        model_total = int(row.get("total_requests") or 0)
        model_success = int(row.get("success_count") or 0)
        model_success_rate = (
            model_success / model_total if model_total else 0.0
        )
        by_model.append(
            ModelMetrics(
                model=row.get("model") or "unknown",
                total_requests=model_total,
                success_rate=round(model_success_rate, 4),
                avg_latency_ms=row.get("avg_latency_ms"),
                avg_tokens=row.get("avg_tokens"),
                avg_cost_usd=row.get("avg_cost_usd"),
            )
        )

    return MetricsResponse(summary=summary, by_model=by_model)
