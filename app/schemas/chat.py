from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str


class SourceReference(BaseModel):
    reference: str
    file_name: str
    page_number: int
    chunk_number: int
    score: float = Field(ge=0, le=1)


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference] = Field(default_factory=list)
