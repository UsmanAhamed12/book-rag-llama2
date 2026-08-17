from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pypdf import PdfReader

from app.api.dependencies.auth import get_current_user
from app.core.container import container
from app.db.postgres import SessionLocal, ensure_schema
from app.models.database.document import DocumentDB
from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter()


@router.post(
    "/",
    response_model=UploadResponse,
)
def upload_pdf(
    file: Annotated[UploadFile, File(...)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    user_id = int(current_user["sub"])

    ensure_schema()

    # Save PDF file
    upload_service = UploadService()

    pdf_path, file_size, file_hash = upload_service.save(file)

    reader = PdfReader(str(pdf_path))
    page_count = len(reader.pages)

    # Save document metadata to PostgreSQL
    db = SessionLocal()

    existing_document = (
        db.query(DocumentDB).filter(DocumentDB.file_hash == file_hash).first()
    )

    if existing_document:
        db.close()

        raise HTTPException(
            status_code=409,
            detail="This PDF has already been uploaded.",
        )

    try:
        document = DocumentDB(
            user_id=user_id,
            filename=file.filename,
            file_hash=file_hash,
            file_size=file_size,
            page_count=page_count,
            chunks=0,
            status="processing",
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        chunks = container.ingestion_service.ingest(
            pdf_path=str(pdf_path),
            document_id=str(document.id),
            user_id=user_id,
            source=str(pdf_path),
        )

        document.chunks = chunks
        document.status = "completed"
        document.summary_status = "processing"

        db.commit()

        try:
            summary, topics = (
                container.document_profile_service.build_profile(
                    user_id=user_id,
                    document_id=str(document.id),
                    filename=document.filename,
                )
            )

            document.summary = summary
            document.topics = topics
            document.summary_status = "completed"

        except Exception:
            document.summary_status = "failed"

        db.commit()

    except Exception:
        if "document" in locals():
            db.rollback()

            document.status = "failed"

            db.commit()

        raise

    finally:
        db.close()

    return UploadResponse(
        filename=file.filename,
        chunks=chunks,
        message="PDF indexed successfully",
    )
