from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    create_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password : str

class userOut(BaseModel):
    id: int
    email : EmailStr
    create_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
