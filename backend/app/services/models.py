from app.core.models import list_known_models
from app.core.pricing import get_pricing_table
from app.schemas.models import ModelInfo, ModelListResponse


def list_models() -> ModelListResponse:
    pricing = get_pricing_table()
    items: list[ModelInfo] = []
    for name in list_known_models():
        model_pricing = pricing.get(name, {})
        items.append(
            ModelInfo(
                name=name,
                input_cost_per_1k=model_pricing.get("input"),
                output_cost_per_1k=model_pricing.get("output"),
            )
        )
    return ModelListResponse(items=items)
