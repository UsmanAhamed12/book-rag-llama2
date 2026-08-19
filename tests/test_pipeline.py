from pathlib import Path

from app.ingestion.pipeline import IngestionPipeline


def test_pipeline_runs() -> None:
    pdf_path = Path("tests/fixtures/sample.pdf")

    pipeline = IngestionPipeline()

    document, chunks = pipeline.ingest(
        str(pdf_path),
    )

    assert document is not None
    assert isinstance(chunks, list)
