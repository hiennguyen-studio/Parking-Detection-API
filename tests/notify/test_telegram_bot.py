"""
Basic test for Telegram bot
"""
import pytest
from src.notify.telegram_bot import TelegramBot


@pytest.fixture
def telegram_bot():
    """Fixture for Telegram bot"""
    return TelegramBot(token="test-token", chat_id="123456")


def test_telegram_bot_initialization(telegram_bot):
    """Test Telegram bot initialization"""
    assert telegram_bot is not None
    assert telegram_bot.token == "test-token"
    assert telegram_bot.chat_id == "123456"


@pytest.mark.unit
def test_telegram_send_message(telegram_bot):
    """Test sending message"""
    # TODO: Implement test
    pass
