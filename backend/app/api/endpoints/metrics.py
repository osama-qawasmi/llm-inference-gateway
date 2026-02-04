from fastapi import APIRouter

from app.schemas.metrics import MetricsResponse
from app.services.metrics import get_metrics

router = APIRouter()


@router.get("/metrics", response_model=MetricsResponse)
def metrics() -> MetricsResponse:
    return get_metrics()
