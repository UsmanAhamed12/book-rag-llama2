import shutil
from pathlib import Path

from fastapi import UploadFile


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
    ) -> tuple[Path, int]:

        file_path = self.upload_dir / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        file_size = file_path.stat().st_size

        return file_path, file_size
