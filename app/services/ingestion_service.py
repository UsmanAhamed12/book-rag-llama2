from app.embeddings.embedding_service import EmbeddingService
from app.ingestion.chunkers.recursive_chunker import RecursiveChunker
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.cleaners.text_cleaner import TextCleaner
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
    ) -> int:

        # Load PDF
        loader = PDFLoader(pdf_path)

        text = loader.load()


        # Clean text
        cleaner = TextCleaner()

        cleaned_text = cleaner.clean(text)


        # Create chunks
        chunker = RecursiveChunker(
            document_id=pdf_path
        )

        chunks = chunker.split(
            cleaned_text
        )


        # Generate embeddings
        embeddings = (
            self.embedding_service
            .embed_chunks(chunks)
        )


        # Store in Chroma
        self.vector_store.add(
            chunks,
            embeddings,
        )


        return len(chunks)