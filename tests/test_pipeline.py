from app.core.settings import settings
from app.ingestion.pipeline import IngestionPipeline


def test_pipeline_runs() -> None:
    pipeline = IngestionPipeline()

    document, chunks = pipeline.ingest(settings.book_path)

    assert document.file_name.endswith(".pdf")
    assert document.document_id != ""
    assert len(chunks) > 0
    assert chunks[0].text != ""