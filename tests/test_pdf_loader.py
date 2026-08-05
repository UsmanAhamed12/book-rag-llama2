# from app.core.settings import settings
# from app.ingestion.loaders.pdf_loader import PDFLoader


# def test_pdf_loader_reads_book():
#     loader = PDFLoader(settings.book_path)

#     text = loader.load()

#     assert isinstance(text, str)
#     assert len(text) > 1000


from app.core.settings import settings
from app.ingestion.loaders.pdf_loader import PDFLoader


def test_pdf_loader_reads_pages() -> None:
    loader = PDFLoader(settings.book_path)

    documents = loader.load()

    assert len(documents) > 0
    assert documents[0].page_number == 1
    assert len(documents[0].text) > 0