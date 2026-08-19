from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.sentence_transformer_provider import SentenceTransformerProvider
from app.llm.service import LLMService
from app.retrieval.retriever import Retriever
from app.services.document_profile_service import DocumentProfileService
from app.services.document_service import DocumentService
from app.services.ingestion_service import IngestionService
from app.vectorstores.chroma_store import ChromaVectorStore


class Container:
    """
    Creates application-wide services once.
    """

    def __init__(self) -> None:
        self.embedding_provider = SentenceTransformerProvider()

        self.embedding_service = EmbeddingService(
            self.embedding_provider,
        )

        self.vector_store = ChromaVectorStore()

        self.ingestion_service = IngestionService(
            self.embedding_service,
            self.vector_store,
        )

        self.retriever = Retriever(
            self.embedding_provider,
        )

        self.llm = LLMService()

        self.document_profile_service = DocumentProfileService(
            retriever=self.retriever,
            llm=self.llm,
        )

        self.document_service = DocumentService(
            self.vector_store,
        )


container = Container()
