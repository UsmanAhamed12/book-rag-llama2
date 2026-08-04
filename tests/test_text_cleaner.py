from app.ingestion.cleaners.text_cleaner import TextCleaner


def test_clean_text():
    raw = "Hello     World\n\n\nPython\tRAG"

    cleaned = TextCleaner.clean(raw)

    assert cleaned == "Hello World\n\nPython RAG"