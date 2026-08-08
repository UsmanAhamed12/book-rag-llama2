from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.core.container import container
from app.db.postgres import SessionLocal
from app.models.database.chat import ChatHistory
from app.schemas.chat import ChatRequest, ChatResponse

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
    current_user: Annotated[dict, Depends(get_current_user)],
):

    session = (
    container.chat_memory_service
    .create_session(
        user_id=int(current_user["sub"])
    )
)

    answer_payload = container.rag_pipeline.ask(
        session_id=session.id,
        question=request.question,
    )

    answer = answer_payload["answer"]

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
        answer=answer,
        sources=answer_payload["sources"],
    )
