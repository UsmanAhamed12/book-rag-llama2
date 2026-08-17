from pathlib import Path

from sqlalchemy.orm import Session

from app.models.database.document import DocumentDB
from app.vectorstores.chroma_store import ChromaVectorStore


class DocumentService:
    def __init__(
        self,
        vector_store: ChromaVectorStore,
    ) -> None:
        self.vector_store = vector_store

    def get_all(
        self,
        db: Session,
        user_id: int,
    ) -> list[DocumentDB]:

        return (
            db.query(DocumentDB)
            .filter(
                DocumentDB.user_id == user_id,
            )
            .order_by(
                DocumentDB.created_at.desc(),
            )
            .all()
        )

    def delete(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ) -> DocumentDB | None:

        document = (
            db.query(DocumentDB)
            .filter(
                DocumentDB.id == document_id,
                DocumentDB.user_id == user_id,
            )
            .first()
        )

        if not document:
            return None

        # Delete embeddings from Chroma
        self.vector_store.delete_by_document_id(
            str(document.id),
        )

        # Delete physical PDF
        pdf_path = Path("data/uploads") / document.filename

        if pdf_path.exists():
            pdf_path.unlink()

        # Delete PostgreSQL record
        db.delete(document)
        db.commit()

        return document

