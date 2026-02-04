from pydantic import BaseModel


class ModelInfo(BaseModel):
    name: str
    input_cost_per_1k: float | None = None
    output_cost_per_1k: float | None = None


class ModelListResponse(BaseModel):
    items: list[ModelInfo]
