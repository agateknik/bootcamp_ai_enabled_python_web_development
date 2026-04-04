from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.models.database import ChatSession
from app.models.engine import get_db

session_router = APIRouter(prefix="/chat-sessions")


@session_router.post("/")
def create_session(db_session: Session = Depends(get_db)):
    new_session = ChatSession()
    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)

    return new_session
