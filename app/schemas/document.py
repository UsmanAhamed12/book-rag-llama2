from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    filename: str
    file_hash: str | None
    file_size: int
    page_count: int
    chunks: int
    status: str
    summary: str | None
    topics: list[str] | None
    summary_status: str
    created_at: datetime
    updated_at: datetime
