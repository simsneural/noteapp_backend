
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str]
    role: Optional[str]

class NoteCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class NoteOut(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    user_id: uuid.UUID

    class Config:
        orm_mode = True
