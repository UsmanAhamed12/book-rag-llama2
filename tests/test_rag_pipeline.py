from app.llm.ollama_client import OllamaClient
from app.rag.pipeline import RAGPipeline


class DummyRetriever:
    def search(self, query, top_k):
        return [
            type(
                "Result",
                (),
                {
                    "text": "Data is information stored and processed.",
                    "metadata": {"document_id": "doc-1", "chunk_index": 1, "page_number": 2},
                },
            )()
        ]


class DummyMemory:
    def __init__(self):
        self.saved = []

    def save_message(self, session_id, role, message):
        self.saved.append((session_id, role, message))

    def get_messages(self, session_id):
        return []


class DummyLLM:
    def __init__(self):
        self.prompts = []

    def answer(self, prompt):
        self.prompts.append(prompt)
        return "ok"


def test_build_prompt_returns_string_and_ask_passes_it_to_llm():
    pipeline = RAGPipeline(
        retriever=DummyRetriever(),
        llm=DummyLLM(),
        memory=DummyMemory(),
    )

    prompt = pipeline.build_prompt(session_id=1, question="What is data?")

    assert isinstance(prompt, str)
    assert "What is data?" in prompt
    assert "Retrieved Context:" in prompt

    result = pipeline.ask(session_id=1, question="What is data?")

    assert result["answer"] == "ok"
    assert pipeline.llm.prompts[0] == prompt


def test_generate_returns_fallback_when_ollama_is_unavailable(monkeypatch):
    def raise_connection_error(*args, **kwargs):
        raise ConnectionError("Failed to connect")

    monkeypatch.setattr("app.llm.ollama_client.ollama.chat", raise_connection_error)

    client = OllamaClient(model="dummy")
    response = client.generate("What is data?")

    assert isinstance(response, str)
    assert response
    assert "fallback" in response.lower() or "data" in response.lower()
