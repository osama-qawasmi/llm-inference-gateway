from fastapi import APIRouter

from app.schemas.models import ModelListResponse
from app.services.models import list_models

router = APIRouter()


@router.get("/models", response_model=ModelListResponse)
def get_models() -> ModelListResponse:
    return list_models()
