from pydantic import BaseModel


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    is_available: bool
