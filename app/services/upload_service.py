from pathlib import Path
import shutil

from fastapi import UploadFile

from app.core import settings


class UploadService:
    """Handles PDF uploads."""

    def __init__(
        self,
        upload_dir: str = "data/uploads",
    ) -> None:

        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        file: UploadFile,
    ) -> Path:

        file_path = self.upload_dir / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return file_path