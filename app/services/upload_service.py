import hashlib
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
    ) -> tuple[Path, int, str]:

        filename = file.filename or "uploaded.pdf"
        file_path = self.upload_dir / filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        file_size = file_path.stat().st_size

        file_hash = self.calculate_hash(file_path)

        return file_path, file_size, file_hash

    @staticmethod
    def calculate_hash(
        file_path: Path,
    ) -> str:

        sha256 = hashlib.sha256()

        with file_path.open("rb") as file:
            for chunk in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                sha256.update(chunk)

        return sha256.hexdigest()
