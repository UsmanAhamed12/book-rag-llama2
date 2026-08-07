from pathlib import Path
from uuid import uuid4

from app.ingestion.chunkers.recursive_chunker import RecursiveChunker
from app.ingestion.cleaners.text_cleaner import TextCleaner
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.models.chunk import Chunk
from app.models.document import Document


class IngestionPipeline:
    """Loads, cleans and chunks a document."""

    def ingest(self, pdf_path: str) -> tuple[Document, list[Chunk]]:
        loader = PDFLoader(pdf_path)
        cleaner = TextCleaner()

        # Load PDF pages
        pages = loader.load()

        # Merge all page text
        raw_text = "\n\n".join(page.text for page in pages)

        # Clean merged text
        clean_text = cleaner.clean(raw_text)

        # Create document metadata
        document = Document(
            document_id=str(uuid4()),
            file_name=Path(pdf_path).name,
            file_path=Path(pdf_path),
        )

        # Chunk cleaned text
        chunker = RecursiveChunker(
            document_id=document.document_id,
            source=str(pdf_path),
        )

        chunks = chunker.split(clean_text)

        return document, chunks