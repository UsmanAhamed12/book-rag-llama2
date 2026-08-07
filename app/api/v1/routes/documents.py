from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


document_service = DocumentService()


@router.get("/")
def get_documents(
    db: Annotated[Session, Depends(get_db)],
):

    documents = document_service.get_all(db)

    return documents


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Annotated[Session, Depends(get_db)],
):

    document = document_service.delete(
        db,
        document_id,
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
