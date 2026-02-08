from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class TaskRequest(BaseModel):
    title: str
    user_id: UUID
    
class TaskResponse(BaseModel):
    id: UUID
    title: str
    is_done: bool
    user_id: str
    created_at: datetime

class TaskUpdate(BaseModel):
    title: str | None = None
    is_done: bool
     