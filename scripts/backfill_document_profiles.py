from app.core.container import container
from app.db.postgres import SessionLocal
from app.models.database.document import DocumentDB
from app.models.database.user import UserDB  # noqa: F401


def main() -> None:
    db = SessionLocal()

    try:
        documents = (
            db.query(DocumentDB)
            .filter(
                DocumentDB.status == "completed",
            )
            .all()
        )

        for document in documents:
            print(
                f"Profiling {document.filename}...",
            )

            document.summary_status = "processing"
            db.commit()

            try:
                summary, topics = (
                    container.document_profile_service.build_profile(
                        user_id=document.user_id,
                        document_id=str(document.id),
                        filename=document.filename,
                    )
                )

                document.summary = summary
                document.topics = topics
                document.summary_status = "completed"

                db.commit()

                print(
                    f"Completed: {document.filename}",
                )

            except Exception as exc:
                document.summary_status = "failed"

                db.commit()

                print(
                    f"Failed: {document.filename}: {exc}",
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()