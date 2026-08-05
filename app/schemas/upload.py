from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    chunks: int
    message: str