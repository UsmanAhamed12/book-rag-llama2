from typing import TypedDict

from fastapi import APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class MessageResponse(TypedDict):
    message: str


@router.post("/")
async def ask_question() -> MessageResponse:
    return {"message": "Coming soon"}
