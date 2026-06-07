"""
User schemas for API
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    """Create user schema"""
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
