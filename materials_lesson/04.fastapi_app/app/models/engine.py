from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///db_library.db"
engine = create_engine(DATABASE_URL)


def get_db():
    with Session(engine) as session:
        yield session
