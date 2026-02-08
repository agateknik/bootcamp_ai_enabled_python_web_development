from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(nullable=False)
    email: str = Field(unique=True)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)

class Task(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    title: str = Field(nullable=False)
    is_done: bool = Field(default=False, nullable=False)
    user_id: uuid.UUID = Field(nullable=False, foreign_key="user.id")
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)
    
    