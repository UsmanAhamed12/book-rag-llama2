from app.db.postgres import SessionLocal
from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)
from app.llm.service import LLMService
from app.rag.pipeline import RAGPipeline
from app.retrieval.retriever import Retriever
from app.services.chat_memory_service import ChatMemoryService

db = SessionLocal()

try:
    # Chat memory
    memory = ChatMemoryService(db)

    # Create new conversation
    session = memory.create_session()

    # Embeddings
    embedding = SentenceTransformerProvider()

    # Retriever
    retriever = Retriever(embedding)

    # LLM
    llm = LLMService()

    # RAG pipeline
    rag = RAGPipeline(
        retriever,
        llm,
        memory,
    )

    # First question
    response = rag.ask(
        session_id=session.id,
        question="What is data?",
    )

    print("\n## Answer 1\n")
    print(response["answer"])

    # Second question
    response = rag.ask(
        session_id=session.id,
        question="Explain it in simple terms.",
    )

    print("\n## Answer 2\n")
    print(response["answer"])

    print("\n## Session ID")
    print(session.id)

finally:
    db.close()
