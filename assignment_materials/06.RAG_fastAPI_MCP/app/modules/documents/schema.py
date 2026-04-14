from pydantic import BaseModel


class DocumentChunk(BaseModel):
    id: str
    text: str
    metadata: dict


class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentChunk]


class DocumentDetailResponse(BaseModel):
    id: str
    text: str
    metadata: dict
