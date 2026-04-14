from pydantic import BaseModel, HttpUrl


class UploadFromUrlRequest(BaseModel):
    url: HttpUrl
    chunk_size: int = 500
    overlap: int = 50
    collection_name: str = "documents"


class UploadResponse(BaseModel):
    success: bool
    message: str
    source_file: str
    source_url: str | None = None
    total_chunks: int
    total_text_length: int
