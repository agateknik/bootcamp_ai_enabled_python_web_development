import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date, timedelta
from sqlmodel import Session, select

from app.models.engine import engine
from app.models.database import Book, Member, BorrowingTransaction


def seed_books(session: Session):
    books = [
        Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="978-0-7432-7356-5"),
        Book(title="To Kill a Mockingbird", author="Harper Lee", isbn="978-0-06-112008-4"),
        Book(title="1984", author="George Orwell", isbn="978-0-452-28423-4"),
        Book(title="Pride and Prejudice", author="Jane Austen", isbn="978-0-14-143951-8"),
        Book(title="The Catcher in the Rye", author="J.D. Salinger", isbn="978-0-316-76948-0"),
        Book(title="Harry Potter and the Sorcerer's Stone", author="J.K. Rowling", isbn="978-0-59-035342-7"),
        Book(title="The Lord of the Rings", author="J.R.R. Tolkien", isbn="978-0-544-00341-5"),
        Book(title="The Hobbit", author="J.R.R. Tolkien", isbn="978-0-545-82893-9"),
        Book(title="The Da Vinci Code", author="Dan Brown", isbn="978-0-307-27767-1"),
        Book(title="The Alchemist", author="Paulo Coelho", isbn="978-0-06-112241-5"),
        Book(title="Educated", author="Tara Westover", isbn="978-0-399-59050-4"),
        Book(title="Becoming", author="Michelle Obama", isbn="978-1-5247-6313-8"),
        Book(title="Sapiens: A Brief History of Humankind", author="Yuval Noah Harari", isbn="978-0-06-231609-7"),
        Book(title="Thinking, Fast and Slow", author="Daniel Kahneman", isbn="978-0-374-27563-1"),
        Book(title="Atomic Habits", author="James Clear", isbn="978-0-7352-1129-2"),
    ]

    for book in books:
        existing = session.exec(select(Book).where(Book.isbn == book.isbn)).first()
        if not existing:
            session.add(book)

    session.commit()
    print(f"Seeded {len(books)} books")
    return books


def seed_members(session: Session):
    members = [
        Member(name="John Anderson", email="john.anderson@gmail.com"),
        Member(name="Sarah Williams", email="sarah.williams@yahoo.com"),
        Member(name="Michael Chen", email="michael.chen@outlook.com"),
        Member(name="Emily Rodriguez", email="emily.rodriguez@hotmail.com"),
        Member(name="David Thompson", email="david.thompson@gmail.com"),
        Member(name="Lisa Park", email="lisa.park@company.com"),
        Member(name="Robert Kim", email="robert.kim@tech.io"),
        Member(name="Jennifer Martinez", email="jennifer.martinez@university.edu"),
        Member(name="Christopher Lee", email="chris.lee@startup.co"),
        Member(name="Amanda Johnson", email="amanda.johnson@design.net"),
    ]

    for member in members:
        existing = session.exec(select(Member).where(Member.email == member.email)).first()
        if not existing:
            session.add(member)

    session.commit()
    print(f"Seeded {len(members)} members")
    return members


def seed_borrowing_transactions(session: Session):
    books = session.exec(select(Book)).all()
    members = session.exec(select(Member)).all()

    if len(books) < 10 or len(members) < 5:
        print("Not enough books or members to seed transactions")
        return

    today = date.today()
    transactions_data = [
        {"book_idx": 0, "member_idx": 0, "borrow_days": 45, "returned": True},
        {"book_idx": 1, "member_idx": 1, "borrow_days": 30, "returned": True},
        {"book_idx": 2, "member_idx": 2, "borrow_days": 60, "returned": True},
        {"book_idx": 3, "member_idx": 3, "borrow_days": 14, "returned": True},
        {"book_idx": 4, "member_idx": 0, "borrow_days": 21, "returned": True},
        {"book_idx": 5, "member_idx": 4, "borrow_days": 90, "returned": True},
        {"book_idx": 6, "member_idx": 5, "borrow_days": 7, "returned": True},
        {"book_idx": 7, "member_idx": 1, "borrow_days": 120, "returned": True},
        {"book_idx": 0, "member_idx": 2, "borrow_days": 15, "returned": False},
        {"book_idx": 8, "member_idx": 6, "borrow_days": 10, "returned": False},
        {"book_idx": 9, "member_idx": 7, "borrow_days": 5, "returned": False},
        {"book_idx": 10, "member_idx": 3, "borrow_days": 3, "returned": False},
        {"book_idx": 11, "member_idx": 8, "borrow_days": 20, "returned": False},
    ]

    count = 0
    for data in transactions_data:
        borrow_date = today - timedelta(days=data["borrow_days"])
        return_date = borrow_date + timedelta(days=14) if data["returned"] else None

        transaction = BorrowingTransaction(
            book_id=books[data["book_idx"]].id,
            member_id=members[data["member_idx"]].id,
            borrow_date=borrow_date,
            return_date=return_date,
        )
        session.add(transaction)
        count += 1

    session.commit()
    print(f"Seeded {count} borrowing transactions")


def main():
    with Session(engine) as session:
        seed_books(session)
        seed_members(session)
        seed_borrowing_transactions(session)
    print("Seeding completed!")


if __name__ == "__main__":
    main()
