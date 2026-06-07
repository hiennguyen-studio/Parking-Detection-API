"""
Camera schemas for API
"""
from pydantic import BaseModel
from datetime import datetime


class CameraCreate(BaseModel):
    """Create camera schema"""
    name: str
    location: str
    stream_url: str


class CameraResponse(BaseModel):
    """Camera response schema"""
    id: int
    name: str
    location: str
    stream_url: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
