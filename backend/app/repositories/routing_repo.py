import json

from app.db.session import get_connection
from app.schemas.routing import RoutingConfig


def get_routing_config() -> RoutingConfig | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT config_json FROM routing_config WHERE id = 1"
        ).fetchone()
    if not row:
        return None
    payload = json.loads(row["config_json"])
    return RoutingConfig(**payload)


def save_routing_config(config: RoutingConfig) -> RoutingConfig:
    payload = json.dumps(config.model_dump())
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO routing_config (id, config_json)
            VALUES (1, ?)
            ON CONFLICT(id) DO UPDATE SET config_json = excluded.config_json
            """,
            (payload,),
        )
        connection.commit()
    return config
