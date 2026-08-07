from pathlib import Path

from app.embeddings.embedding_service import EmbeddingService
from app.ingestion.chunkers.recursive_chunker import RecursiveChunker
from app.ingestion.cleaners.text_cleaner import TextCleaner
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.vectorstores.chroma_store import ChromaVectorStore


class IngestionService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: ChromaVectorStore,
    ) -> None:

        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def ingest(
        self,
        pdf_path: str,
        document_id: str,
        source: str | None = None,
    ) -> int:

        # Load PDF
        loader = PDFLoader(pdf_path)

        pages = loader.load()

        cleaner = TextCleaner()

        # Store a display-safe filename in vector metadata.  This is later
        # returned to the chat client alongside the exact PDF page number.
        source_name = Path(source).name if source else Path(pdf_path).name

        chunker = RecursiveChunker(
            document_id=document_id,
            source=source_name,
        )

        chunks = []

        for page in pages:
            cleaned_text = cleaner.clean(page.text)

            page_chunks = chunker.split(
                cleaned_text,
                page_number=page.page_number,
            )

            chunks.extend(page_chunks)

        # Generate embeddings
        embeddings = self.embedding_service.embed_chunks(chunks)

        # Store in Chroma
        self.vector_store.add(
            chunks,
            embeddings,
        )

        return len(chunks)
