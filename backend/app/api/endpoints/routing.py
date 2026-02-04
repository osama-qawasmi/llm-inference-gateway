from fastapi import APIRouter

from app.schemas.routing import RoutingConfig
from app.services.routing import load_routing_config, update_routing_config

router = APIRouter()


@router.get("/routing", response_model=RoutingConfig)
def get_routing() -> RoutingConfig:
    return load_routing_config()


@router.put("/routing", response_model=RoutingConfig)
def put_routing(config: RoutingConfig) -> RoutingConfig:
    return update_routing_config(config)
