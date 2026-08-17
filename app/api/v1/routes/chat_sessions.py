from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.postgres import get_db
from app.models.database.chat_message import ChatMessageDB
from app.models.database.chat_session import ChatSessionDB
from app.schemas.chat_session import ChatSessionUpdate
from app.services.chat_memory_service import ChatMemoryService

router = APIRouter(
    prefix="/chat/sessions",
    tags=["Chat Sessions"],
)


@router.post("/")
def create_chat_session(
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> dict:
    user_id = int(current_user["sub"])

    memory = ChatMemoryService(db)

    session = memory.create_session(
        user_id=user_id,
    )

    return {
        "id": session.id,
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }


@router.get("/")
def list_chat_sessions(
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> list[dict]:
    user_id = int(current_user["sub"])

    sessions = (
        db.query(ChatSessionDB)
        .filter(ChatSessionDB.user_id == user_id)
        .order_by(ChatSessionDB.created_at.desc())
        .all()
    )

    return [
            {
                "id": session.id,
                "title": session.title,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
            }
            for session in sessions
        ]

@router.get("/{session_id}")
def get_chat_session(
    session_id: int,
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> dict:
    user_id = int(current_user["sub"])

    session = (
        db.query(ChatSessionDB)
        .filter(
            ChatSessionDB.id == session_id,
            ChatSessionDB.user_id == user_id,
        )
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    return {
        "id": session.id,
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }


@router.get("/{session_id}/messages")
def get_chat_messages(
    session_id: int,
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> list[dict]:
    user_id = int(current_user["sub"])

    session = (
        db.query(ChatSessionDB)
        .filter(
            ChatSessionDB.id == session_id,
            ChatSessionDB.user_id == user_id,
        )
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    messages = (
        db.query(ChatMessageDB)
        .filter(ChatMessageDB.session_id == session_id)
        .order_by(ChatMessageDB.id.asc())
        .all()
    )

    return [
        {
            "id": message.id,
            "role": message.role,
            "message": message.message,
            "sources": message.sources or [],
            "created_at": message.created_at,
        }
        for message in messages
    ]

@router.patch("/{session_id}")
def rename_chat_session(
    session_id: int,
    payload: ChatSessionUpdate,
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> dict:
    user_id = int(current_user["sub"])

    memory = ChatMemoryService(db)

    session = memory.rename_session(
        session_id=session_id,
        user_id=user_id,
        title=payload.title,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    return {
        "id": session.id,
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }


@router.delete("/{session_id}")
def delete_chat_session(
    session_id: int,
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> dict:
    user_id = int(current_user["sub"])

    memory = ChatMemoryService(db)

    deleted = memory.delete_session(
        session_id=session_id,
        user_id=user_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    return {
        "message": "Chat session deleted successfully",
        "session_id": session_id,
    }