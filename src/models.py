from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    last_login_date: datetime


class Token(BaseModel):
    username: str
    token: UUID


class Task(BaseModel):
    title: str
    description: str
    priority: Optional[int] = 0
    id: UUID
    user_id: UUID
    completed: Optional[bool]


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int = 0


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
