from pathlib import Path

from app.ingestion.loaders.pdf_loader import PDFLoader


def test_pdf_loader_reads_pages() -> None:
    pdf_path = Path("tests/fixtures/sample.pdf")

    loader = PDFLoader(str(pdf_path))
    pages = loader.load()

    assert len(pages) == 1
    assert pages[0].page_number == 1
