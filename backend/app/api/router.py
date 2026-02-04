from fastapi import APIRouter

from app.api.endpoints import chat, metrics, models, routing, usage

api_router = APIRouter(prefix="/api")
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(models.router, tags=["models"])
api_router.include_router(routing.router, tags=["routing"])
api_router.include_router(usage.router, tags=["usage"])
api_router.include_router(metrics.router, tags=["metrics"])
