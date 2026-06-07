<<<<<<< HEAD
"""
Main application settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Illegal Parking Detection System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "Parking Detection API"
    API_DESCRIPTION: str = "API for illegal parking detection and notification"

    # Database
    DATABASE_URL: str = "sqlite:///./parking_detection.db"
    # PostgreSQL example: "postgresql://user:password@localhost/parking_db"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    TELEGRAM_WEBHOOK_URL: Optional[str] = None
    TELEGRAM_USE_WEBHOOK: bool = False

    # Email
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SENDER_EMAIL: Optional[str] = None

    # File paths
    MODEL_PATH: str = "./data/models/"
    VIDEO_PATH: str = "./data/videos/"
    IMAGE_PATH: str = "./data/images/"
    EVIDENCE_PATH: str = "./data/evidence/"

    # AI Model
    CONFIDENCE_THRESHOLD: float = 0.5
    NMS_THRESHOLD: float = 0.4
    MODEL_NAME: str = "yolov8"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
=======
"""
Main application settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Illegal Parking Detection System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "Parking Detection API"
    API_DESCRIPTION: str = "API for illegal parking detection and notification"

    # Database
    DATABASE_URL: str = "sqlite:///./parking_detection.db"
    # PostgreSQL example: "postgresql://user:password@localhost/parking_db"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    TELEGRAM_WEBHOOK_URL: Optional[str] = None
    TELEGRAM_USE_WEBHOOK: bool = False

    # Email
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SENDER_EMAIL: Optional[str] = None

    # File paths
    MODEL_PATH: str = "./data/models/"
    VIDEO_PATH: str = "./data/videos/"
    IMAGE_PATH: str = "./data/images/"
    EVIDENCE_PATH: str = "./data/evidence/"

    # AI Model
    CONFIDENCE_THRESHOLD: float = 0.5
    NMS_THRESHOLD: float = 0.4
    MODEL_NAME: str = "yolov8"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
