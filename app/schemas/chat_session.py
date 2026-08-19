from pydantic import BaseModel, Field


class ChatSessionUpdate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )
