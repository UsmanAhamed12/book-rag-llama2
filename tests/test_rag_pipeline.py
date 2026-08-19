from app.llm.ollama_client import OllamaClient
from app.rag.pipeline import RAGPipeline


class DummyRetriever:
    def search(self, query, user_id, top_k, document_ids=None):
        return [
            type(
                "Result",
                (),
                {
                    "text": "Data is information stored and processed.",
                    "score": 0.9,
                    "document_id": "doc-1",
                    "page_number": 2,
                    "metadata": {
                        "document_id": "doc-1",
                        "chunk_index": 1,
                        "page_number": 2,
                    },
                },
            )()
        ]


class DummyMemory:
    def __init__(self):
        self.saved = []

    def save_message(
        self,
        session_id,
        user_id,
        role,
        message,
        sources=None,
    ):
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
        session_id,
        user_id,
    ):
        return []


class DummyLLM:
    def __init__(self):
        self.prompts = []

    def answer(self, prompt):
        self.prompts.append(prompt)
        return "ok"

    def rewrite_query(
        self,
        question,
        history,
    ):
        return question


class EmptyRetriever:
    def search(self, query, user_id, top_k, document_ids=None):
        return []


def test_build_prompt_returns_string_and_ask_passes_it_to_llm():
    pipeline = RAGPipeline(retriever=DummyRetriever(), llm=DummyLLM())

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
    assert len(pipeline.llm.prompts) == 1
    assert "What is not in this book?" in pipeline.llm.prompts[0]


def test_generate_returns_fallback_when_ollama_is_unavailable(monkeypatch):
    def raise_connection_error(*args, **kwargs):
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


def test_ask_does_not_generate_an_answer_without_relevant_context():
    llm = DummyLLM()

    pipeline = RAGPipeline(retriever=EmptyRetriever(), llm=llm)

    result = pipeline.ask(
        session_id=1,
        user_id=1,
        question="What is not in this book?",
        memory=DummyMemory(),
    )

    assert result == {
        "answer": "I cannot find this information in the provided book context.",
        "sources": [],
    }

    assert llm.prompts == []
