from pathlib import Path

import fitz

from app.ingestion.cleaners.text_cleaner import TextCleaner


class PDFLoader:
    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)

    def load(self) -> str:
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"{self.pdf_path} does not exist.")

        document = fitz.open(self.pdf_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return TextCleaner.clean(text)
