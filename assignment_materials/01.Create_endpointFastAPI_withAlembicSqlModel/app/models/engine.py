from sqlmodel import create_engine, Session 


SQLITE_URL = "sqlite:///database.db"

engine = create_engine(SQLITE_URL, 
                       connect_args={"check_same_thread": False})

def get_db():
    with Session(engine) as session:
        yield session