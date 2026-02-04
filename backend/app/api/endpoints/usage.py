from fastapi import APIRouter, Query

from app.repositories.usage_repo import list_usage
from app.schemas.usage import UsageListResponse

router = APIRouter()


@router.get("/usage", response_model=UsageListResponse)
def get_usage(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> UsageListResponse:
    return list_usage(limit=limit, offset=offset)
