from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserRequest(BaseModel):
    name : str
    email: str

class UserResponse(BaseModel):    
    id: UUID
    name: str
    email: str
    created_at: datetime
        
    