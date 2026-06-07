"""
Telegram bot for notifications
"""
from typing import Optional, Callable
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import python-telegram-bot
try:
    from telegram import Bot, Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    HAS_TELEGRAM = True
except ImportError:
    HAS_TELEGRAM = False
    logger.warning("python-telegram-bot not installed. Install with: pip install python-telegram-bot")


class TelegramBot:
    """Handle Telegram notifications for parking violations"""

    def __init__(self, token: str, chat_id: str):
        """
        Initialize Telegram bot
        
        Args:
            token: Telegram bot token from BotFather
            chat_id: Chat ID or group ID to send messages to
        """
        self.token = token
        self.chat_id = chat_id
        self.bot = None
        self.app = None
        self.handlers: dict = {}
        self._init_bot()

    def _init_bot(self):
        """Initialize Telegram bot connection"""
        if not HAS_TELEGRAM:
            logger.error("python-telegram-bot not available")
            return
        
        if not self.token:
            logger.error("Telegram token not provided")
            return
        
        try:
            self.bot = Bot(token=self.token)
            logger.info(f"Telegram bot initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Telegram bot: {e}")

    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Send a text message via Telegram

        Args:
            message: Message text
            parse_mode: "HTML" or "Markdown"

        Returns:
            True if successful
        """
        if self.bot is None:
            logger.error("Telegram bot not initialized")
            return False
        
        if not self.chat_id:
            logger.error("Chat ID not provided")
            return False
        
        try:
            import asyncio
            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            ))
            logger.info(f"Message sent to {self.chat_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False

    def send_photo(self, photo_path: str, caption: str = "") -> bool:
        """
        Send a photo via Telegram
        
        Args:
            photo_path: Path to photo file
            caption: Photo caption
            
        Returns:
            True if successful
        """
        if self.bot is None:
            logger.error("Telegram bot not initialized")
            return False
        
        if not Path(photo_path).exists():
            logger.error(f"Photo file not found: {photo_path}")
            return False
        
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            with open(photo_path, "rb") as photo:
                loop.run_until_complete(self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML"
                ))
            logger.info(f"Photo sent to {self.chat_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send photo: {e}")
            return False

    def send_alert(self, violation_data: dict) -> bool:
        """
        Send a formatted parking violation alert
        
        Args:
            violation_data: Dict with violation info:
                - timestamp: Detection time
                - camera: Camera name
                - location: Location name
                - plate_number: License plate (if detected)
                - confidence: Confidence score
                - image_path: Path to evidence image
                
        Returns:
            True if successful
        """
        try:
            # Format alert message
            timestamp = violation_data.get("timestamp", datetime.now().isoformat())
            camera = violation_data.get("camera", "Unknown")
            location = violation_data.get("location", "Unknown")
            plate = violation_data.get("plate_number", "N/A")
            confidence = violation_data.get("confidence", 0)
            
            message = f"""
🚗 <b>ILLEGAL PARKING DETECTED</b>

📍 <b>Location:</b> {location}
📹 <b>Camera:</b> {camera}
⏰ <b>Time:</b> {timestamp}
🔖 <b>Plate:</b> {plate}
📊 <b>Confidence:</b> {confidence:.1%}

⚠️ Please check the evidence image below.
"""
            
            # Send text alert
            self.send_message(message)
            
            # Send evidence image if available
            image_path = violation_data.get("image_path")
            if image_path and Path(image_path).exists():
                caption = f"Evidence from {camera} at {timestamp}"
                self.send_photo(image_path, caption)
            
            logger.info(f"Alert sent for violation: {plate}")
            return True
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
            return False

    def send_statistics(self, stats: dict) -> bool:
        """
        Send system statistics
        
        Args:
            stats: Statistics dict with camera names and violation counts
            
        Returns:
            True if successful
        """
        try:
            message = "<b>📊 System Statistics</b>\n\n"
            for cam_name, count in stats.items():
                message += f"📹 {cam_name}: {count} violations\n"
            
            return self.send_message(message)
        except Exception as e:
            logger.error(f"Failed to send statistics: {e}")
            return False

    def register_handler(self, command: str, handler: Callable):
        """Register a command handler"""
        self.handlers[command] = handler
        logger.info(f"Handler registered for command: /{command}")

    def get_info(self) -> dict:
        """Get bot information"""
        return {
            "token": self.token[:10] + "***" if self.token else None,
            "chat_id": self.chat_id,
            "initialized": self.bot is not None,
            "handlers": list(self.handlers.keys())
        }

    def __del__(self):
        """Cleanup"""
        if self.bot is not None:
            self.bot = None
