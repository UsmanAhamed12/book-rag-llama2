from typing import TypedDict

from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


class MessageResponse(TypedDict):
    message: str


@router.get("/")
async def list_documents() -> MessageResponse:
    return {"message": "Coming soon"}
