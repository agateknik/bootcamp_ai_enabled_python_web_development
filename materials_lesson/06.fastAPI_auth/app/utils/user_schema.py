from pydantic import BaseModel


class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    name: str
    email: str
    password: str
