<<<<<<< HEAD
"""
Violation schemas for API
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ViolationCreate(BaseModel):
    """Create violation schema"""
    camera_id: int
    plate_number: str
    confidence: float
    image_path: str
    latitude: float
    longitude: float


class ViolationResponse(BaseModel):
    """Violation response schema"""
    id: int
    camera_id: int
    plate_number: str
    confidence: float
    image_path: str
    is_confirmed: bool
    created_at: datetime

    class Config:
        from_attributes = True
=======
"""
Violation schemas for API
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ViolationCreate(BaseModel):
    """Create violation schema"""
    camera_id: int
    plate_number: str
    confidence: float
    image_path: str
    latitude: float
    longitude: float


class ViolationResponse(BaseModel):
    """Violation response schema"""
    id: int
    camera_id: int
    plate_number: str
    confidence: float
    image_path: str
    is_confirmed: bool
    created_at: datetime

    class Config:
        from_attributes = True
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
