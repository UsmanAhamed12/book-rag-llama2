import re


class TextCleaner:
    """Clean extracted PDF text."""

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove tabs
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Remove more than two consecutive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
