from pydantic import BaseModel, Field, ConfigDict


class Source(BaseModel):
    page: int | None = None
    relevance: float
    text: str


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    pages_indexed: int
    chunks_indexed: int
    size_bytes: int


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    document_id: str = Field(min_length=1, max_length=64)
    question: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
