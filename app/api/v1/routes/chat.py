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

    rag_pipeline = RAGPipeline(
        retriever=container.retriever,
        llm=container.llm,
    )

    # ---------------------------------------------------------
    # Document-profile summary path
    # ---------------------------------------------------------
    if (
        request.document_ids
        and rag_pipeline.is_document_summary_request(
            request.question,
        )
    ):
        documents = container.document_service.get_by_ids(
            db=db,
            user_id=user_id,
            document_ids=request.document_ids,
        )

        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No selected documents were found.",
            )

        profile_parts: list[str] = []

        for document in documents:
            topics = ", ".join(
                document.topics or [],
            )

            summary = (
                document.summary
                or "No stored summary is available for this document."
            )

            profile_parts.append(
                
                    f"Filename: {document.filename}\n\n"
                    f"Summary:\n{summary}\n\n"
                    f"Topics:\n{topics or 'No topics available.'}"
                
            )

        profiles = "\n\n---\n\n".join(
            profile_parts,
        )

        answer = (
            container.llm.summarize_document_profiles(
                question=request.question,
                profiles=profiles,
            )
        )

        memory.save_message(
            session_id=request.session_id,
            user_id=user_id,
            role="user",
            message=request.question,
        )

        memory.save_message(
            session_id=request.session_id,
            user_id=user_id,
            role="assistant",
            message=answer,
            sources=[],
        )

        return ChatResponse(
            answer=answer,
            sources=[],
        )

    # ---------------------------------------------------------
    # Normal RAG path
    # ---------------------------------------------------------
    answer_payload = rag_pipeline.ask(
        session_id=request.session_id,
        user_id=user_id,
        question=request.question,
        memory=memory,
        document_ids=request.document_ids,
    )

    return ChatResponse(
        answer=answer_payload["answer"],
        sources=answer_payload["sources"],
    )