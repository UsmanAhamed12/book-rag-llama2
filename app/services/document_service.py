from sqlalchemy.orm import Session

from app.models.database.document import DocumentDB


class DocumentService:


    def get_all(
        self,
        db: Session,
    ):

        return (
            db.query(DocumentDB)
            .all()
        )


    def delete(
        self,
        db: Session,
        document_id: int,
    ):

        document = (
            db.query(DocumentDB)
            .filter(
                DocumentDB.id == document_id
            )
            .first()
        )


        if document:

            db.delete(document)
            db.commit()


        return document