from typing import Any

from pytest import MonkeyPatch

from app.llm.ollama_client import OllamaClient
from app.llm.service import LLMService
from app.models.database.chat_message import ChatMessageDB
from app.rag.pipeline import RAGAnswerPayload, RAGPipeline
from app.retrieval.models import RetrievalResult
from app.retrieval.retriever import Retriever
from app.services.chat_memory_service import ChatMemoryService


class DummyRetriever(Retriever):
    def __init__(self) -> None:
        pass

    def search(
        self,
        query: str,
        user_id: int,
        document_ids: list[str] | None = None,
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:
        del query, user_id, document_ids, top_k, score_threshold
        return [
            RetrievalResult(
                text="Data is information stored and processed.",
                score=0.9,
                document_id="doc-1",
                page_number=2,
                metadata={
                    "document_id": "doc-1",
                    "chunk_index": 1,
                    "page_number": 2,
                },
            )
        ]


class DummyMemory(ChatMemoryService):
    def __init__(self) -> None:
        self.saved: list[dict[str, Any]] = []

    def save_message(
        self,
        session_id: int,
        user_id: int,
        role: str,
        message: str,
        sources: list[dict[str, Any]] | None = None,
    ) -> None:
        self.saved.append(
            {
                "session_id": session_id,
                "user_id": user_id,
                "role": role,
                "message": message,
                "sources": sources,
            }
        )

    def get_messages(
        self,
        session_id: int,
        user_id: int,
    ) -> list[ChatMessageDB]:
        del session_id, user_id
        return []


class DummyLLM(LLMService):
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def answer(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return "ok"

    def rewrite_query(
        self,
        question: str,
        history: str,
    ) -> str:
        del history
        return question


class EmptyRetriever(Retriever):
    def __init__(self) -> None:
        pass

    def search(
        self,
        query: str,
        user_id: int,
        document_ids: list[str] | None = None,
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:
        del query, user_id, document_ids, top_k, score_threshold
        return []


def test_build_prompt_returns_string_and_ask_passes_it_to_llm() -> None:
    llm = DummyLLM()
    pipeline = RAGPipeline(retriever=DummyRetriever(), llm=llm)

    prompt, results = pipeline.build_prompt(
        session_id=1, user_id=1, question="What is data?", memory=DummyMemory()
    )

    assert isinstance(prompt, str)
    assert len(results) == 1
    assert "What is data?" in prompt
    assert "Retrieved Context:" in prompt

    memory = DummyMemory()

    result = pipeline.ask(
        session_id=1,
        user_id=1,
        question="What is not in this book?",
        memory=memory,
    )

    assert result["answer"] == "ok"
    assert result["sources"] == [
        {
            "reference": "S1",
            "file_name": "doc-1",
            "page_number": 2,
            "chunk_number": 1,
            "score": 0.9,
        }
    ]
    assert len(llm.prompts) == 1
    assert "What is not in this book?" in llm.prompts[0]


def test_generate_returns_fallback_when_ollama_is_unavailable(
    monkeypatch: MonkeyPatch,
) -> None:
    def raise_connection_error(*args: object, **kwargs: object) -> None:
        raise ConnectionError("Failed to connect")

    monkeypatch.setattr(
        "app.llm.ollama_client.ollama.chat",
        raise_connection_error,
    )

    client = OllamaClient(model="dummy")
    response = client.generate("What is data?")

    assert isinstance(response, str)
    assert response
    assert "fallback" in response.lower() or "data" in response.lower()


def test_ask_does_not_generate_an_answer_without_relevant_context() -> None:
    llm = DummyLLM()

    pipeline = RAGPipeline(retriever=EmptyRetriever(), llm=llm)

    result = pipeline.ask(
        session_id=1,
        user_id=1,
        question="What is not in this book?",
        memory=DummyMemory(),
    )

    expected: RAGAnswerPayload = {
        "answer": "I cannot find this information in the provided book context.",
        "sources": [],
    }
    assert result == expected

    assert llm.prompts == []
