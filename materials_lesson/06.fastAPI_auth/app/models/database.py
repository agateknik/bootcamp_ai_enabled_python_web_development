from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(nullable=False)
    email: str = Field(unique=True)
    password: str = Field(nullable=True)
    role: str = Field(default="user", nullable=False)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)
    tasks: list["Task"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all,delete"}
    )


class Task(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    title: str = Field(nullable=False)
    is_done: bool = Field(default=False, nullable=False)
    user_id: uuid.UUID = Field(
        nullable=False, foreign_key="user.id", ondelete="CASCADE"
    )
    user: User = Relationship(
        back_populates="tasks", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)
