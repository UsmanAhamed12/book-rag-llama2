from app.retrieval.retriever import Retriever


class DummyEmbeddingProvider:
    def embed(self, texts):
        return [[0.1, 0.2] for _ in texts]


class DummyCollection:
    def query(self, **kwargs):
        return {
            "documents": [["closest", "farthest"]],
            "distances": [[0.1, 2.0]],
            "metadatas": [
                [
                    {"document_id": "doc", "page_number": 4},
                    {"document_id": "doc", "page_number": 9},
                ]
            ],
        }


def test_retriever_returns_best_similarity_first(monkeypatch):
    monkeypatch.setattr(
        "app.retrieval.retriever.get_chroma_client",
        lambda: type(
            "Client",
            (),
            {"get_or_create_collection": lambda *args, **kwargs: DummyCollection()},
        )(),
    )
    retriever = Retriever(DummyEmbeddingProvider())

    results = retriever.search(
        "query",
        user_id=1,
        top_k=2,
    )

    assert [result.text for result in results] == ["closest", "farthest"]
    assert results[0].score > results[1].score
