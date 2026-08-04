from app.core.settings import settings
from app.ingestion.loaders.pdf_loader import PDFLoader

loader = PDFLoader(settings.book_path)

text = loader.load()

print("=" * 60)
print(text[:1000])
print("=" * 60)
print(f"Characters: {len(text)}")
