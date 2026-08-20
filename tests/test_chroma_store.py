from app.vectorstores.chroma_store import ChromaVectorStore


def test_chroma_creation() -> None:
    store = ChromaVectorStore("test_collection")

    assert store.collection is not None
