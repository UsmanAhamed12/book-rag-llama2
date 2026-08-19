from typing import Annotated, TypedDict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.container import container
from app.db.postgres import get_db
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.types.auth import CurrentUser

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService(
    container.vector_store,
)


class DeleteDocumentResponse(TypedDict):
    message: str
    document_id: int


@router.get("/", response_model=list[DocumentResponse])
def get_documents(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> list[DocumentResponse]:
    user_id = int(current_user["sub"])

    documents = document_service.get_all(
        db,
        user_id,
    )

    return [DocumentResponse.model_validate(document) for document in documents]


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> DeleteDocumentResponse:
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
