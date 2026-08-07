from pathlib import Path
from uuid import uuid4

import fitz

from app.models.document import Document
from app.models.page import Page

# from app.ingestion.cleaners.text_cleaner import TextCleaner


class PDFLoader:
    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)
        self._resolve_path()

    def _resolve_path(self) -> None:
        if self.pdf_path.exists():
            return

        if self.pdf_path.suffix.lower() != ".pdf":
            candidate = self.pdf_path.with_suffix(".pdf")
            if candidate.exists():
                self.pdf_path = candidate
                return

        if self.pdf_path.name != "Data_Engineering.pdf":
            alt_name = self.pdf_path.with_name(self.pdf_path.name.replace("_", " "))
            if alt_name.exists():
                self.pdf_path = alt_name
                return

        if self.pdf_path.parent.exists():
            matches = sorted(self.pdf_path.parent.glob("*.pdf"))
            if matches:
                self.pdf_path = matches[0]

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