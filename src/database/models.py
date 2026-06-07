<<<<<<< HEAD
"""
Database models using SQLAlchemy
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    violations = relationship("Violation", back_populates="user")


class Camera(Base):
    """Camera model"""
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    location = Column(String)
    stream_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    violations = relationship("Violation", back_populates="camera")


class Violation(Base):
    """Parking violation model"""
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    plate_number = Column(String, index=True)
    confidence = Column(Float)
    image_path = Column(String)
    video_path = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    camera = relationship("Camera", back_populates="violations")
    user = relationship("User", back_populates="violations")
=======
"""
Database models using SQLAlchemy
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    violations = relationship("Violation", back_populates="user")


class Camera(Base):
    """Camera model"""
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    location = Column(String)
    stream_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    violations = relationship("Violation", back_populates="camera")


class Violation(Base):
    """Parking violation model"""
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    plate_number = Column(String, index=True)
    confidence = Column(Float)
    image_path = Column(String)
    video_path = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    camera = relationship("Camera", back_populates="violations")
    user = relationship("User", back_populates="violations")
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
