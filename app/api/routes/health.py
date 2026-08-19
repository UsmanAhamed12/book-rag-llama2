from typing import TypedDict

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


class HealthResponse(TypedDict):
    status: str
    service: str


@router.get("/")
async def health_check() -> HealthResponse:
    return {
        "status": "healthy",
        "service": "book-rag-api",
    }
