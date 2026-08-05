from fastapi import APIRouter, File, UploadFile

from app.core.container import container
from app.db.postgres import SessionLocal
from app.models.database.document import DocumentDB
from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService


router = APIRouter()


@router.post(
    "/",
    response_model=UploadResponse,
)
def upload_pdf(
    file: UploadFile = File(...),
):

    # Save PDF file
    upload_service = UploadService()

    pdf_path = upload_service.save(
        file
    )


    # Ingest PDF
    chunks = (
        container.ingestion_service
        .ingest(
            str(pdf_path)
        )
    )


    # Save document metadata to PostgreSQL
    db = SessionLocal()

    try:

        document = DocumentDB(
            filename=file.filename,
            chunks=chunks,
        )

        db.add(document)

        db.commit()

    finally:

        db.close()


    return UploadResponse(
        filename=file.filename,
        chunks=chunks,
        message="PDF indexed successfully",
    )