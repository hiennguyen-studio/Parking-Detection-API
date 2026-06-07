"""API route handlers"""

from .violations import router as violations_router
from .cameras import router as cameras_router
from .users import router as users_router
from .statistics import router as statistics_router

__all__ = ["violations_router", "cameras_router", "users_router", "statistics_router"]
