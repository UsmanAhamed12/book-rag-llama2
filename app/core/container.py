from app.db.postgres import (
    SessionLocal,
)
from app.embeddings.embedding_service import (
    EmbeddingService,
)
from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)
from app.llm.service import (
    LLMService,
)
from app.rag.pipeline import (
    RAGPipeline,
)
from app.retrieval.retriever import (
    Retriever,
)
from app.services.chat_memory_service import (
    ChatMemoryService,
)
from app.services.ingestion_service import (
    IngestionService,
)
from app.vectorstores.chroma_store import (
    ChromaVectorStore,
)


class Container:
    """
    Creates application services once.
    """

    def __init__(self) -> None:

        # Embedding model
        self.embedding_provider = SentenceTransformerProvider()

        self.embedding_service = EmbeddingService(self.embedding_provider)

        # Vector database
        self.vector_store = ChromaVectorStore()

        # Ingestion pipeline
        self.ingestion_service = IngestionService(
            self.embedding_service,
            self.vector_store,
        )

        # Retrieval
        self.retriever = Retriever(self.embedding_provider)

        # LLM
        self.llm = LLMService()

        # Chat memory
        self.chat_memory_service = ChatMemoryService(SessionLocal())

        # RAG
        self.rag_pipeline = RAGPipeline(
            self.retriever,
            self.llm,
            self.chat_memory_service,
        )


container = Container()
