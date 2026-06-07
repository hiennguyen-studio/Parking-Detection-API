<<<<<<< HEAD
# Telegram Bot Configuration and Usage

## Overview

The Telegram Bot module provides real-time alerts for parking violations detected by the system.

## Setup

### 1. Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/start` and then `/newbot`
3. Follow the prompts to create a new bot
4. Copy the **API Token** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Get Your Chat ID

1. Open Telegram and search for **@RawDataBot**
2. Send any message to it
3. Copy the `chat` -> `id` value (a number, e.g., 123456789)

### 3. Configure Environment

Edit `.env` file:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
TELEGRAM_WEBHOOK_URL=https://your-domain.com/telegram/webhook (optional)
TELEGRAM_USE_WEBHOOK=False  # Set to True if using webhook
```

## Features

### Polling vs Webhook

#### Polling Mode (Default)
- Bot continuously checks Telegram servers for messages
- Simpler to set up
- Recommended for development

#### Webhook Mode (Production)
- Telegram sends updates to your server directly
- Requires HTTPS and public URL
- Better performance and reliability

### Alert Format

```
🚨 Cảnh báo vi phạm đỗ xe trái phép

📍 Vị trí: Intersection A
⏰ Thời gian: 2024-01-15 14:30:00
📹 Camera: Camera 1
🚗 Biển số xe: 30A12345
🔗 Bằng chứng: [Xem chi tiết]
```

## Usage

### Sending Alerts Programmatically

```python
from src.notify.telegram_bot import TelegramBot
from src.config.settings import settings

# Initialize bot
bot = TelegramBot(
    token=settings.TELEGRAM_BOT_TOKEN,
    chat_id=settings.TELEGRAM_CHAT_ID
)

# Send alert
violation_data = {
    "location": "Intersection A",
    "timestamp": "2024-01-15 14:30:00",
    "camera_name": "Camera 1",
    "plate_number": "30A12345",
    "evidence_url": "http://your-domain.com/evidence/123"
}

bot.send_alert(violation_data)
```

### Integrating with FastAPI

```python
from fastapi import APIRouter
from src.notify.telegram_bot import TelegramBot
from src.config.settings import settings

router = APIRouter()
bot = TelegramBot(
    token=settings.TELEGRAM_BOT_TOKEN,
    chat_id=settings.TELEGRAM_CHAT_ID
)

@router.post("/violations")
async def create_violation(violation: ViolationCreate):
    # ... create violation in database ...
    
    # Send alert to Telegram
    await bot.send_alert(violation_data)
    
    return violation_response
```

## Webhook Setup (Optional)

If using webhook mode:

1. Generate SSL certificate:
```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```

2. Add webhook endpoint to FastAPI:
```python
@app.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    # Process Telegram update
    await bot.handle_webhook(update)
    return {"ok": True}
```

3. Register webhook with Telegram:
```bash
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://your-domain.com/telegram/webhook", "certificate": "@cert.pem"}' \
  https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook
```

## Commands and Interactions

### Bot Commands

```
/start - Start using the bot
/help - Show help message
/status - Get system status
/violations - Get recent violations
```

### Inline Buttons (Optional)

```python
# Example: Confirmation buttons
markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("Confirm", callback_data="confirm_123"),
     InlineKeyboardButton("Reject", callback_data="reject_123")]
])

bot.send_message(
    message="Confirm this violation?",
    reply_markup=markup
)
```

## Testing

### Test Bot Connection

```python
from src.notify.telegram_bot import TelegramBot
from src.config.settings import settings

bot = TelegramBot(
    token=settings.TELEGRAM_BOT_TOKEN,
    chat_id=settings.TELEGRAM_CHAT_ID
)

# Send test message
result = bot.send_message("Test message from Parking Detection System")
print(f"Success: {result}")
```

### Test with curl

```bash
# Get bot info
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe

# Send test message
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage \
  -d "chat_id=<YOUR_CHAT_ID>" \
  -d "text=Test message"
```

## Troubleshooting

### Bot Not Receiving Messages

1. Check TELEGRAM_BOT_TOKEN is correct
2. Check TELEGRAM_CHAT_ID is correct
3. Verify bot has permission to send messages
4. Check firewall/network restrictions

### Message Formatting Issues

Ensure you're using the correct parse_mode:
- `HTML` (default) - Use `<b>`, `<i>`, `<a>` tags
- `Markdown` - Use `*bold*`, `_italic_`

### Rate Limiting

Telegram has rate limits. If you get "Too many requests":
- Implement exponential backoff retry logic
- Consider batching messages
- Use a message queue (e.g., Celery)

## References

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [BotFather Commands](https://core.telegram.org/bots#botfather)
- [Webhook Documentation](https://core.telegram.org/bots/webhooks)
=======
# Telegram Bot Configuration and Usage

## Overview

The Telegram Bot module provides real-time alerts for parking violations detected by the system.

## Setup

### 1. Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/start` and then `/newbot`
3. Follow the prompts to create a new bot
4. Copy the **API Token** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Get Your Chat ID

1. Open Telegram and search for **@RawDataBot**
2. Send any message to it
3. Copy the `chat` -> `id` value (a number, e.g., 123456789)

### 3. Configure Environment

Edit `.env` file:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
TELEGRAM_WEBHOOK_URL=https://your-domain.com/telegram/webhook (optional)
TELEGRAM_USE_WEBHOOK=False  # Set to True if using webhook
```

## Features

### Polling vs Webhook

#### Polling Mode (Default)
- Bot continuously checks Telegram servers for messages
- Simpler to set up
- Recommended for development

#### Webhook Mode (Production)
- Telegram sends updates to your server directly
- Requires HTTPS and public URL
- Better performance and reliability

### Alert Format

```
🚨 Cảnh báo vi phạm đỗ xe trái phép

📍 Vị trí: Intersection A
⏰ Thời gian: 2024-01-15 14:30:00
📹 Camera: Camera 1
🚗 Biển số xe: 30A12345
🔗 Bằng chứng: [Xem chi tiết]
```

## Usage

### Sending Alerts Programmatically

```python
from src.notify.telegram_bot import TelegramBot
from src.config.settings import settings

# Initialize bot
bot = TelegramBot(
    token=settings.TELEGRAM_BOT_TOKEN,
    chat_id=settings.TELEGRAM_CHAT_ID
)

# Send alert
violation_data = {
    "location": "Intersection A",
    "timestamp": "2024-01-15 14:30:00",
    "camera_name": "Camera 1",
    "plate_number": "30A12345",
    "evidence_url": "http://your-domain.com/evidence/123"
}

bot.send_alert(violation_data)
```

### Integrating with FastAPI

```python
from fastapi import APIRouter
from src.notify.telegram_bot import TelegramBot
from src.config.settings import settings

router = APIRouter()
bot = TelegramBot(
    token=settings.TELEGRAM_BOT_TOKEN,
    chat_id=settings.TELEGRAM_CHAT_ID
)

@router.post("/violations")
async def create_violation(violation: ViolationCreate):
    # ... create violation in database ...
    
    # Send alert to Telegram
    await bot.send_alert(violation_data)
    
    return violation_response
```

## Webhook Setup (Optional)

If using webhook mode:

1. Generate SSL certificate:
```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```

2. Add webhook endpoint to FastAPI:
```python
@app.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    # Process Telegram update
    await bot.handle_webhook(update)
    return {"ok": True}
```

3. Register webhook with Telegram:
```bash
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://your-domain.com/telegram/webhook", "certificate": "@cert.pem"}' \
  https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook
```

## Commands and Interactions

### Bot Commands

```
/start - Start using the bot
/help - Show help message
/status - Get system status
/violations - Get recent violations
```

### Inline Buttons (Optional)

```python
# Example: Confirmation buttons
markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("Confirm", callback_data="confirm_123"),
     InlineKeyboardButton("Reject", callback_data="reject_123")]
])

bot.send_message(
    message="Confirm this violation?",
    reply_markup=markup
)
```

## Testing

### Test Bot Connection

```python
from src.notify.telegram_bot import TelegramBot
from src.config.settings import settings

bot = TelegramBot(
    token=settings.TELEGRAM_BOT_TOKEN,
    chat_id=settings.TELEGRAM_CHAT_ID
)

# Send test message
result = bot.send_message("Test message from Parking Detection System")
print(f"Success: {result}")
```

### Test with curl

```bash
# Get bot info
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe

# Send test message
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage \
  -d "chat_id=<YOUR_CHAT_ID>" \
  -d "text=Test message"
```

## Troubleshooting

### Bot Not Receiving Messages

1. Check TELEGRAM_BOT_TOKEN is correct
2. Check TELEGRAM_CHAT_ID is correct
3. Verify bot has permission to send messages
4. Check firewall/network restrictions

### Message Formatting Issues

Ensure you're using the correct parse_mode:
- `HTML` (default) - Use `<b>`, `<i>`, `<a>` tags
- `Markdown` - Use `*bold*`, `_italic_`

### Rate Limiting

Telegram has rate limits. If you get "Too many requests":
- Implement exponential backoff retry logic
- Consider batching messages
- Use a message queue (e.g., Celery)

## References

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [BotFather Commands](https://core.telegram.org/bots#botfather)
- [Webhook Documentation](https://core.telegram.org/bots/webhooks)
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
