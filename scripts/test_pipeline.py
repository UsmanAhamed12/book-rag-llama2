from app.core.settings import settings
from app.ingestion.pipeline import IngestionPipeline

pipeline = IngestionPipeline()

document, chunks = pipeline.ingest(settings.book_path)

print(document)
print()

print(f"Chunks: {len(chunks)}")
print()

print(chunks[0])