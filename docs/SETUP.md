<<<<<<< HEAD
# Setup and Installation Guide

## Prerequisites

- Python 3.9+
- PostgreSQL 12+ (optional, SQLite is default)
- Docker and Docker Compose (optional)
- Telegram Bot Token (for notifications)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Important: Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
```

### 5. Initialize Database

```bash
# Using SQLite (default)
python scripts/setup_db.py

# Using PostgreSQL
# Update DATABASE_URL in .env to: postgresql://user:password@localhost/parking_db
# Then run:
python scripts/setup_db.py
```

### 6. Load Sample Data (optional)

```bash
python scripts/init_data.py
```

### 7. Run the Application

```bash
# Development mode
python -m uvicorn src.backend.main:app --reload

# Production mode
python -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## Docker Setup

### Using Docker Compose

```bash
# Navigate to docker directory
cd docker

# Create .env file in project root with Telegram credentials
# Then run:
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop containers
docker-compose down
```

### Manual Docker Commands

```bash
# Build image
docker build -f docker/Dockerfile -t parking-detection:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./parking_detection.db \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TELEGRAM_CHAT_ID=your_chat_id \
  --name parking-api \
  parking-detection:latest
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/AI/test_detector.py

# Run by marker
pytest -m unit
pytest -m integration
```

## Testing the API

### Using Swagger UI

Open your browser and navigate to: `http://localhost:8000/docs`

### Using curl

```bash
# List violations
curl http://localhost:8000/api/v1/violations

# Get statistics
curl http://localhost:8000/api/v1/statistics/summary

# Health check
curl http://localhost:8000/health
```

### Using Python requests

```python
import requests

# Get list of violations
response = requests.get('http://localhost:8000/api/v1/violations')
print(response.json())

# Create new violation
violation_data = {
    "camera_id": 1,
    "plate_number": "30A12345",
    "confidence": 0.95,
    "image_path": "/path/to/image.jpg",
    "latitude": 21.0285,
    "longitude": 105.8542
}
response = requests.post('http://localhost:8000/api/v1/violations', json=violation_data)
print(response.json())
```

## Troubleshooting

### Database Connection Error

```
Error: Could not connect to database
```

**Solution**: Check DATABASE_URL in .env file and ensure PostgreSQL is running

### Telegram Bot Not Sending Alerts

```
Error: Telegram notification failed
```

**Solution**: 
1. Verify TELEGRAM_BOT_TOKEN is correct
2. Verify TELEGRAM_CHAT_ID is correct (should be numeric)
3. Check bot has permission to send messages

### Port Already in Use

```
Error: Address already in use
```

**Solution**: Change API_PORT in .env or kill process using port 8000

## Next Steps

1. Configure Telegram bot (see [TELEGRAM_BOT.md](TELEGRAM_BOT.md))
2. Set up camera streams
3. Train or download AI models
4. Deploy to production (see [ARCHITECTURE.md](ARCHITECTURE.md))
=======
# Setup and Installation Guide

## Prerequisites

- Python 3.9+
- PostgreSQL 12+ (optional, SQLite is default)
- Docker and Docker Compose (optional)
- Telegram Bot Token (for notifications)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Important: Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
```

### 5. Initialize Database

```bash
# Using SQLite (default)
python scripts/setup_db.py

# Using PostgreSQL
# Update DATABASE_URL in .env to: postgresql://user:password@localhost/parking_db
# Then run:
python scripts/setup_db.py
```

### 6. Load Sample Data (optional)

```bash
python scripts/init_data.py
```

### 7. Run the Application

```bash
# Development mode
python -m uvicorn src.backend.main:app --reload

# Production mode
python -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## Docker Setup

### Using Docker Compose

```bash
# Navigate to docker directory
cd docker

# Create .env file in project root with Telegram credentials
# Then run:
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop containers
docker-compose down
```

### Manual Docker Commands

```bash
# Build image
docker build -f docker/Dockerfile -t parking-detection:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./parking_detection.db \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TELEGRAM_CHAT_ID=your_chat_id \
  --name parking-api \
  parking-detection:latest
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/AI/test_detector.py

# Run by marker
pytest -m unit
pytest -m integration
```

## Testing the API

### Using Swagger UI

Open your browser and navigate to: `http://localhost:8000/docs`

### Using curl

```bash
# List violations
curl http://localhost:8000/api/v1/violations

# Get statistics
curl http://localhost:8000/api/v1/statistics/summary

# Health check
curl http://localhost:8000/health
```

### Using Python requests

```python
import requests

# Get list of violations
response = requests.get('http://localhost:8000/api/v1/violations')
print(response.json())

# Create new violation
violation_data = {
    "camera_id": 1,
    "plate_number": "30A12345",
    "confidence": 0.95,
    "image_path": "/path/to/image.jpg",
    "latitude": 21.0285,
    "longitude": 105.8542
}
response = requests.post('http://localhost:8000/api/v1/violations', json=violation_data)
print(response.json())
```

## Troubleshooting

### Database Connection Error

```
Error: Could not connect to database
```

**Solution**: Check DATABASE_URL in .env file and ensure PostgreSQL is running

### Telegram Bot Not Sending Alerts

```
Error: Telegram notification failed
```

**Solution**: 
1. Verify TELEGRAM_BOT_TOKEN is correct
2. Verify TELEGRAM_CHAT_ID is correct (should be numeric)
3. Check bot has permission to send messages

### Port Already in Use

```
Error: Address already in use
```

**Solution**: Change API_PORT in .env or kill process using port 8000

## Next Steps

1. Configure Telegram bot (see [TELEGRAM_BOT.md](TELEGRAM_BOT.md))
2. Set up camera streams
3. Train or download AI models
4. Deploy to production (see [ARCHITECTURE.md](ARCHITECTURE.md))
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
