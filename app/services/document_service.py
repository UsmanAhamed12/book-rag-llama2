from sqlalchemy.orm import Session

from app.models.database.document import DocumentDB


class DocumentService:
    def get_all(
        self,
        db: Session,
        user_id: int,
    ):
        return db.query(DocumentDB).filter(DocumentDB.user_id == user_id).all()

    def delete(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ):
        document = (
            db.query(DocumentDB)
            .filter(
                DocumentDB.id == document_id,
                DocumentDB.user_id == user_id,
            )
            .first()
        )

        if document:
            db.delete(document)
            db.commit()

        return document
