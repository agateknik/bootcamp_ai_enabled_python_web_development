from sqlmodel import Session, select
from fastapi import APIRouter, Depends

from app.models.engine import get_db
from app.models.database import Book
from app.schema.book_schema import BookResponse

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.get("", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    query = select(Book)
    books = db.exec(query).all()
    return books


@books_router.get("/{id}", response_model=BookResponse)
def get_book_id(id: int, db: Session = Depends(get_db)):
    book = db.get(Book, id)
    return book
