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
        document_id: str,
    ) -> int:

        # Load PDF
        loader = PDFLoader(pdf_path)

        pages = loader.load()

        cleaner = TextCleaner()

        chunker = RecursiveChunker(
            document_id=document_id
        )

        chunks = []

        for page in pages:
            cleaned_text = cleaner.clean(page.text)

            page_chunks = chunker.split(cleaned_text)

            chunks.extend(page_chunks)


        # Generate embeddings
        embeddings = (
            self.embedding_service
            .embed_chunks(chunks)
        )

        print("Chunks:", len(chunks))
        print("Embeddings:", len(embeddings))
        print(chunks[0])


        # Store in Chroma
        self.vector_store.add(
            chunks,
            embeddings,
        )


        return len(chunks)