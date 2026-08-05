from fastapi import APIRouter

from app.core.container import container
from app.db.postgres import SessionLocal
from app.models.database.chat import ChatHistory

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    answer = (
        container.rag_pipeline
        .ask(
            request.question
        )
    )

    db = SessionLocal()

    try:

        history = ChatHistory(
            question=request.question,
            answer=answer,
        )

        db.add(history)

        db.commit()

    finally:

        db.close()


    return ChatResponse(
        answer=answer
    )