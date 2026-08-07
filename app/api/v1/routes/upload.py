from typing import Annotated

from fastapi import APIRouter, File, UploadFile

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
):

    ensure_schema()

    # Save PDF file
    upload_service = UploadService()

    pdf_path, file_size = upload_service.save(file)

    # Save document metadata to PostgreSQL
    db = SessionLocal()

    try:
        document = DocumentDB(
            filename=file.filename,
            file_size=file_size,
            page_count=0,
            chunks=0,
            status="processing",
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        chunks = container.ingestion_service.ingest(
            str(pdf_path),
            str(document.id),
            str(pdf_path),
        )

        document.chunks = chunks
        document.status = "completed"

        db.commit()
    except Exception:
        if "document" in locals():
            document.status = "failed"
            db.rollback()
            db.commit()

        raise

    finally:
        db.close()

    return UploadResponse(
        filename=file.filename,
        chunks=chunks,
        message="PDF indexed successfully",
    )
