from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    isbn: str
    borrowing_records: list["BorrowingTransaction"] = Relationship(back_populates="book")

    @property
    def is_available(self):
        # jika tidak ada satupun record yang return_datenya None maka tidak available, 
        return not any([record.return_date is None for record in self.borrowing_records])


class Member(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    borrowing_records: list["BorrowingTransaction"] = Relationship(back_populates="member")


class BorrowingTransaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    borrow_date: date
    return_date: date | None = Field(default=None)

    book_id: int = Field(foreign_key="book.id")
    book: Book = Relationship(back_populates="borrowing_records")

    member_id: int = Field(foreign_key="member.id")
    member: Member = Relationship(back_populates="borrowing_records")
