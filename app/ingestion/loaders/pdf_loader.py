from pathlib import Path
from uuid import uuid4

import fitz

from app.models.document import Document
from app.models.page import Page

# from app.ingestion.cleaners.text_cleaner import TextCleaner


class PDFLoader:
    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)

    def load(self) -> list[Page]:
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"{self.pdf_path} does not exist.")

        with fitz.open(self.pdf_path) as document:
            pages: list[Page] = []

            for page_number, page in enumerate(document, start=1):
                pages.append(
                    Page(
                        text=page.get_text(),
                        page_number=page_number,
                        source=self.pdf_path.name,
                    )
                )

            return pages
        # document = fitz.open(self.pdf_path)

        # documents: list[Document] = []

        # for page_number, page in enumerate(document, start=1):
        #     documents.append(
        #         Document(
        #             text=page.get_text(),
        #             page_number=page_number,
        #             source=self.pdf_path.name,
        #         )
        #     )

        # return documents

        # document.close()

        # cleaned_text = TextCleaner.clean(text)
        # return [Document(content=cleaned_text)]