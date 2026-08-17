from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.container import container
from app.db.postgres import get_db
from app.rag.pipeline import RAGPipeline
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_memory_service import ChatMemoryService

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
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> ChatResponse:

    user_id = int(current_user["sub"])

    memory = ChatMemoryService(db)

    session = memory.get_session(
        session_id=request.session_id,
        user_id=user_id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found.",
        )

    # rag_pipeline = RAGPipeline(
    #     retriever=container.retriever,
    #     llm=container.llm,
    # )

    rag_pipeline = RAGPipeline(
        retriever=container.retriever,
        llm=container.llm,
    )

    answer_payload = rag_pipeline.ask(
        session_id=request.session_id,
        user_id=user_id,
        question=request.question,
        memory=memory,
    )

    return ChatResponse(
        answer=answer_payload["answer"],
        sources=answer_payload["sources"],
    )