from app.core.config import settings
from app.repositories.routing_repo import get_routing_config, save_routing_config
from app.schemas.routing import RoutingConfig


def load_routing_config() -> RoutingConfig:
    config = get_routing_config()
    if config:
        return config
    default = RoutingConfig(default_model=settings.default_model)
    return save_routing_config(default)


def update_routing_config(config: RoutingConfig) -> RoutingConfig:
    return save_routing_config(config)


def select_model(message: str) -> str:
    config = load_routing_config()
    for rule in sorted(config.rules, key=lambda item: item.max_characters):
        if len(message) <= rule.max_characters:
            return rule.model
    return config.default_model
