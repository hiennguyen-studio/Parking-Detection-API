"""
Utility helpers
"""
from datetime import datetime


def format_timestamp(dt: datetime) -> str:
    """Format datetime to string"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_current_time() -> datetime:
    """Get current datetime"""
    return datetime.utcnow()


def parse_timestamp(ts: str) -> datetime:
    """Parse timestamp string to datetime"""
    return datetime.fromisoformat(ts)
