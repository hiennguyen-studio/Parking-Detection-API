"""
Pydantic schemas for database
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: str


class UserCreate(UserBase):
    """User creation schema"""
    password: str


class UserResponse(UserBase):
    """User response schema"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CameraBase(BaseModel):
    """Base camera schema"""
    name: str
    location: str
    stream_url: str


class CameraCreate(CameraBase):
    """Camera creation schema"""
    pass


class CameraResponse(CameraBase):
    """Camera response schema"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ViolationBase(BaseModel):
    """Base violation schema"""
    camera_id: int
    plate_number: str
    confidence: float


class ViolationCreate(ViolationBase):
    """Violation creation schema"""
    image_path: str
    latitude: float
    longitude: float


class ViolationResponse(ViolationBase):
    """Violation response schema"""
    id: int
    user_id: Optional[int]
    image_path: str
    is_confirmed: bool
    created_at: datetime

    class Config:
        from_attributes = True
