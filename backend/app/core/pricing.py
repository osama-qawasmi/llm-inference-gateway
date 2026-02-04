import json

from app.core.config import settings

DEFAULT_PRICING: dict[str, dict[str, float]] = {}


def get_pricing_table() -> dict[str, dict[str, float]]:
    if not settings.model_pricing_json:
        return DEFAULT_PRICING
    try:
        payload = json.loads(settings.model_pricing_json)
    except json.JSONDecodeError:
        return DEFAULT_PRICING
    if not isinstance(payload, dict):
        return DEFAULT_PRICING
    return payload


def estimate_cost_usd(
    model: str,
    input_tokens: int | None,
    output_tokens: int | None,
) -> float | None:
    pricing_table = get_pricing_table()
    pricing = pricing_table.get(model)
    if not pricing:
        pricing = _match_pricing(model, pricing_table)
    if not pricing:
        return None
    input_rate = float(pricing.get("input", 0.0))
    output_rate = float(pricing.get("output", 0.0))
    if input_tokens is None and output_tokens is None:
        return None
    input_cost = (input_tokens or 0) / 1000.0 * input_rate
    output_cost = (output_tokens or 0) / 1000.0 * output_rate
    return round(input_cost + output_cost, 6)


def _match_pricing(
    model: str, pricing_table: dict[str, dict[str, float]]
) -> dict[str, float] | None:
    if not model:
        return None
    candidates = [
        key for key in pricing_table.keys() if model.startswith(key)
    ]
    if not candidates:
        return None
    best_key = max(candidates, key=len)
    return pricing_table.get(best_key)
