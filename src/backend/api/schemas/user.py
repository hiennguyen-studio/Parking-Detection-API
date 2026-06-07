<<<<<<< HEAD
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
=======
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
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
