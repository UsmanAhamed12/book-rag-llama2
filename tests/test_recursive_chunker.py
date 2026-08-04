from app.ingestion.chunkers.recursive_chunker import RecursiveChunker


def test_chunker_creates_chunks():
    text = "A" * 5000

    chunker = RecursiveChunker(
        document_id="book-1",
        chunk_size=800,
        overlap=150,
    )

    chunks = chunker.split(text)

    assert len(chunks) > 1
    assert chunks[0].document_id == "book-1"
    assert chunks[0].chunk_index == 0
