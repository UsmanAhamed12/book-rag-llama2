from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.container import container
from app.db.postgres import get_db
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService(
    container.vector_store,
)


@router.get("/")
def get_documents(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):

    user_id = int(current_user["sub"])

    documents = document_service.get_all(
        db,
        user_id,
    )

    return documents


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):

    user_id = int(current_user["sub"])

    document = document_service.delete(
        db,
        document_id,
        user_id,
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {
        "message": "Document deleted successfully",
        "document_id": document_id,
    }
