from fastapi import FastAPI

from app.core.logging import logger
from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.on_event("startup")
async def startup_event():
    logger.info("Application started.")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")
    return {
        "message": "Book RAG API",
        "environment": settings.environment,
        "model": settings.ollama_model,
    }