from dataclasses import dataclass

from app.core.config import settings
from app.services.routing import load_routing_config


@dataclass(frozen=True)
class RoutingDecision:
    model: str
    reason: str
    rule_index: int | None = None


def resolve_model(message: str, requested_model: str | None) -> RoutingDecision:
    if requested_model:
        return RoutingDecision(model=requested_model, reason="explicit")

    config = load_routing_config()
    for index, rule in enumerate(sorted(config.rules, key=lambda item: item.max_characters)):
        if len(message) <= rule.max_characters:
            return RoutingDecision(model=rule.model, reason="rule", rule_index=index)

    default_model = config.default_model or settings.default_model
    return RoutingDecision(model=default_model, reason="default")
