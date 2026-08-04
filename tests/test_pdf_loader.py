from app.ingestion.loaders.pdf_loader import PDFLoader
from pathlib import Path
from app.core.settings import settings





def test_pdf_loader_reads_book():
    loader = PDFLoader(settings.book_path)

    text = loader.load()

    assert isinstance(text, str)
    assert len(text) > 1000