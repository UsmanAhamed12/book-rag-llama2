from pathlib import Path

import chromadb
from chromadb.api import ClientAPI

from app.core.settings import settings


def get_chroma_client() -> ClientAPI:
    path = Path(settings.chroma_path)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return chromadb.PersistentClient(
        path=str(path),
    )
