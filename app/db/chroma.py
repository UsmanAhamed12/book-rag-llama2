from pathlib import Path

import chromadb

from app.core.settings import settings


def get_chroma_client():
    path = Path(settings.chroma_path)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return chromadb.PersistentClient(
        path=str(path)
    )