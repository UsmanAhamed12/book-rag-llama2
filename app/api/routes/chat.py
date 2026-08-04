from fastapi import APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/")
async def ask_question():
    return {
        "message": "Coming soon"
    }