# Hệ Thống Phát Hiện Và Cảnh Báo Đỗ Xe Trái Phép
## Illegal Parking Detection and Alert System

A comprehensive system for detecting and alerting illegal parking violations using AI and computer vision.

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed information about the project layout.

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL or SQLite
- OpenCV
- PyTorch or TensorFlow

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the System

```bash
python src/backend/main.py
```

## Components

- **AI/ML**: Machine learning models for vehicle and parking violation detection using YOLOv8
- **Camera**: Video stream processing and real-time frame analysis
- **User**: User management, registration, and JWT authentication
- **Notify**: Multi-channel notifications (Telegram, Email)
- **Backend**: FastAPI REST API with comprehensive endpoints
- **Database**: SQLAlchemy ORM with PostgreSQL/SQLite support
- **Dashboard**: Web UI for monitoring and management
- **Utils**: Validators, helpers, and utility functions

## Key Features

- ✅ **Real-time Detection**: YOLOv8 AI model for vehicle detection
- ✅ **Telegram Alerts**: Instant notifications via Telegram Bot
- ✅ **Web Dashboard**: Modern UI for violations, cameras, and statistics
- ✅ **RESTful API**: Comprehensive API endpoints for all operations
- ✅ **Database**: Efficient data storage with SQLAlchemy ORM
- ✅ **Docker Support**: Easy deployment with Docker and Docker Compose
- ✅ **CI/CD Ready**: GitHub Actions workflows for testing and deployment
- ✅ **Fully Documented**: Complete API docs and setup guides

## Documentation

See the [docs](docs/) folder for detailed documentation.

## Testing

Run tests with:
```bash
pytest tests/
```

## License

MIT License

## Contributors

Your Team Name
