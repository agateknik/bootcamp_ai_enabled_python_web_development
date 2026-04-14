from pydantic import BaseModel


class SearchResultMetadata(BaseModel):
    source_file: str
    source_path: str
    chunk_index: int
    chunk_position: float
    token_count: int
    keywords: list[str]
    topics: list[str]
    language: str


class SearchResultItem(BaseModel):
    id: str
    rank: int
    score: float
    text: str
    metadata: SearchResultMetadata


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResultItem]
