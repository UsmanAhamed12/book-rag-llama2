from fastapi import FastAPI

from app.api.router import api_router
from app.core.logging import logger
from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Application started.")
    