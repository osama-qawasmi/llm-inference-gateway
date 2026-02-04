from fastapi import FastAPI

from app.api.router import api_router
from app.api.v1.router import api_router as api_v1_router
from app.core.config import settings
from app.db.session import init_db

app = FastAPI(title=settings.app_name)
app.include_router(api_router)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def startup() -> None:
    init_db()
