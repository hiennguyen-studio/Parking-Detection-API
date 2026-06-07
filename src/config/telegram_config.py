"""
Telegram configuration
"""
from typing import Optional
from pydantic import BaseModel


class TelegramConfig(BaseModel):
    """Telegram Bot configuration"""

    TOKEN: Optional[str] = None
    CHAT_ID: Optional[str] = None
    WEBHOOK_URL: Optional[str] = None
    USE_WEBHOOK: bool = False
    POLLING_TIMEOUT: int = 30

    # Message templates
    VIOLATION_ALERT_TEMPLATE: str = (
        "🚨 <b>Cảnh báo vi phạm đỗ xe trái phép</b>\n\n"
        "📍 <b>Vị trí:</b> {location}\n"
        "⏰ <b>Thời gian:</b> {timestamp}\n"
        "📹 <b>Camera:</b> {camera_name}\n"
        "🚗 <b>Biển số xe:</b> {plate_number}\n"
        "🔗 <b>Bằng chứng:</b> <a href='{evidence_url}'>Xem chi tiết</a>\n"
    )

    CONFIRMATION_TEMPLATE: str = (
        "✅ Cảnh báo đã được gửi\n"
        "📌 ID sự kiện: {event_id}\n"
        "👤 Quản lý: {admin_name}"
    )

    class Config:
        case_sensitive = True
