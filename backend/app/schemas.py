from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from app.models import ReviewStatus


# Auth
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Chat
class SessionCreate(BaseModel):
    title: Optional[str] = "New Chat"


class SessionOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    session_id: int
    message: str


# Review
class ReviewOut(BaseModel):
    id: int
    query: str
    response: Optional[str]
    reason: Optional[str]
    status: ReviewStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class ReviewUpdate(BaseModel):
    status: ReviewStatus
    response: Optional[str] = None
