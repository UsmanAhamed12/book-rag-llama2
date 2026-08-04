from pathlib import Path
from uuid import uuid4

from app.ingestion.chunkers.recursive_chunker import RecursiveChunker
from app.ingestion.cleaners.text_cleaner import TextCleaner
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.models.document import Document
from app.models.chunk import Chunk


class IngestionPipeline:
    """Loads, cleans and chunks a document."""

    def ingest(self, pdf_path: str) -> tuple[Document, list[Chunk]]:

        loader = PDFLoader(pdf_path)
        cleaner = TextCleaner()

        raw_text = loader.load()
        clean_text = cleaner.clean(raw_text)

        document = Document(
            document_id=str(uuid4()),
            file_name=Path(pdf_path).name,
            file_path=Path(pdf_path),
            text=clean_text,
        )

        chunker = RecursiveChunker(
            document_id=document.document_id,
        )

        chunks = chunker.split(document.text)

        return document, chunks