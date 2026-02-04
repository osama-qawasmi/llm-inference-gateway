from pydantic import BaseModel, Field


class RoutingRule(BaseModel):
    max_characters: int = Field(ge=1)
    model: str = Field(min_length=1)


class RoutingConfig(BaseModel):
    default_model: str = Field(min_length=1)
    rules: list[RoutingRule] = Field(default_factory=list)
