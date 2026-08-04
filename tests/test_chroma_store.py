from app.vectorstores.chroma_store import ChromaVectorStore


def test_chroma_creation():

    store = ChromaVectorStore(
        "test_collection"
    )

    assert store.collection is not None