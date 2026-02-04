from app.core.config import settings
from app.core.pricing import get_pricing_table


def list_known_models() -> list[str]:
    models = set(get_pricing_table().keys())
    models.add(settings.default_model)
    if settings.openai_model:
        models.add(settings.openai_model)
    return sorted(models)
