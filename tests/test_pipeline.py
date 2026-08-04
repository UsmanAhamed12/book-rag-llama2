from app.core.settings import settings
from app.ingestion.pipeline import IngestionPipeline


def test_pipeline_runs():

    pipeline = IngestionPipeline()

    document, chunks = pipeline.ingest(settings.book_path)

    assert document.file_name.endswith(".pdf")
    assert len(document.text) > 0
    assert len(chunks) > 0