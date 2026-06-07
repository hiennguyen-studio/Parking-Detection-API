<<<<<<< HEAD
# System Architecture

## Overview

The Illegal Parking Detection System is built with a microservices architecture that separates concerns into distinct modules.

## Components

### 1. AI/ML Module (`src/AI/`)
- **ParkingDetector**: Main detector class using YOLOv8
- **ModelManager**: Manages loading and caching of models

### 2. Camera Module (`src/camera/`)
- **CameraHandler**: Handles camera input and stream management
- **StreamProcessor**: Processes video streams in real-time

### 3. User Module (`src/user/`)
- **AuthManager**: Handles JWT authentication and password hashing
- **UserManager**: Manages user accounts and profiles

### 4. Notification Module (`src/notify/`)
- **TelegramBot**: Sends alerts via Telegram
- **EmailService**: Sends email notifications
- **NotificationManager**: Routes notifications to appropriate channels

### 5. Database Module (`src/database/`)
- **DatabaseManager**: Manages database connections
- **Models**: SQLAlchemy ORM models (User, Camera, Violation)

### 6. Backend API (`src/backend/`)
- **FastAPI Application**: RESTful API with endpoints
- **Routes**: API route handlers for violations, cameras, users, statistics
- **Schemas**: Pydantic models for request/response validation
- **Dashboard**: Web UI for monitoring and management

## Data Flow

```
Camera Stream
    ↓
Camera Handler (capture)
    ↓
Stream Processor (process)
    ↓
AI Detector (detect violations)
    ↓
Database (store)
    ↓
├─ Notification Manager
│   ├─ Telegram Bot (instant alert)
│   └─ Email Service (notification)
│
└─ Web Dashboard (visualization)
```

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: PostgreSQL/SQLite + SQLAlchemy ORM
- **Authentication**: JWT + Passlib

### AI/ML
- **Models**: YOLOv8 (Ultralytics)
- **Computer Vision**: OpenCV
- **Deep Learning**: PyTorch

### Notifications
- **Telegram**: python-telegram-bot
- **Email**: aiosmtplib

### DevOps
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Database**: PostgreSQL

## Deployment Architecture

```
┌─────────────────────────────────────┐
│      Load Balancer / Nginx          │
└────────────┬────────────────────────┘
             │
     ┌───────┴────────┐
     │                │
┌────▼──────┐   ┌─────▼──────┐
│ API       │   │ API        │
│ Container │   │ Container  │
│ (FastAPI) │   │ (FastAPI)  │
└────┬──────┘   └─────┬──────┘
     │                │
     └───────┬────────┘
             │
      ┌──────▼──────┐
      │ PostgreSQL  │
      │ Database    │
      └─────────────┘
```

## Security Considerations

1. **JWT Authentication**: All API endpoints protected
2. **Password Hashing**: Bcrypt for secure password storage
3. **Environment Variables**: Sensitive data stored in .env
4. **CORS**: Configured for allowed origins
5. **Docker Isolation**: Services run in isolated containers

## Scalability

- **Horizontal Scaling**: Multiple API instances behind load balancer
- **Database**: PostgreSQL can be optimized with indexing and replication
- **Caching**: Can add Redis for session/cache management
- **Queue System**: Can add Celery for async task processing
=======
# System Architecture

## Overview

The Illegal Parking Detection System is built with a microservices architecture that separates concerns into distinct modules.

## Components

### 1. AI/ML Module (`src/AI/`)
- **ParkingDetector**: Main detector class using YOLOv8
- **ModelManager**: Manages loading and caching of models

### 2. Camera Module (`src/camera/`)
- **CameraHandler**: Handles camera input and stream management
- **StreamProcessor**: Processes video streams in real-time

### 3. User Module (`src/user/`)
- **AuthManager**: Handles JWT authentication and password hashing
- **UserManager**: Manages user accounts and profiles

### 4. Notification Module (`src/notify/`)
- **TelegramBot**: Sends alerts via Telegram
- **EmailService**: Sends email notifications
- **NotificationManager**: Routes notifications to appropriate channels

### 5. Database Module (`src/database/`)
- **DatabaseManager**: Manages database connections
- **Models**: SQLAlchemy ORM models (User, Camera, Violation)

### 6. Backend API (`src/backend/`)
- **FastAPI Application**: RESTful API with endpoints
- **Routes**: API route handlers for violations, cameras, users, statistics
- **Schemas**: Pydantic models for request/response validation
- **Dashboard**: Web UI for monitoring and management

## Data Flow

```
Camera Stream
    ↓
Camera Handler (capture)
    ↓
Stream Processor (process)
    ↓
AI Detector (detect violations)
    ↓
Database (store)
    ↓
├─ Notification Manager
│   ├─ Telegram Bot (instant alert)
│   └─ Email Service (notification)
│
└─ Web Dashboard (visualization)
```

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: PostgreSQL/SQLite + SQLAlchemy ORM
- **Authentication**: JWT + Passlib

### AI/ML
- **Models**: YOLOv8 (Ultralytics)
- **Computer Vision**: OpenCV
- **Deep Learning**: PyTorch

### Notifications
- **Telegram**: python-telegram-bot
- **Email**: aiosmtplib

### DevOps
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Database**: PostgreSQL

## Deployment Architecture

```
┌─────────────────────────────────────┐
│      Load Balancer / Nginx          │
└────────────┬────────────────────────┘
             │
     ┌───────┴────────┐
     │                │
┌────▼──────┐   ┌─────▼──────┐
│ API       │   │ API        │
│ Container │   │ Container  │
│ (FastAPI) │   │ (FastAPI)  │
└────┬──────┘   └─────┬──────┘
     │                │
     └───────┬────────┘
             │
      ┌──────▼──────┐
      │ PostgreSQL  │
      │ Database    │
      └─────────────┘
```

## Security Considerations

1. **JWT Authentication**: All API endpoints protected
2. **Password Hashing**: Bcrypt for secure password storage
3. **Environment Variables**: Sensitive data stored in .env
4. **CORS**: Configured for allowed origins
5. **Docker Isolation**: Services run in isolated containers

## Scalability

- **Horizontal Scaling**: Multiple API instances behind load balancer
- **Database**: PostgreSQL can be optimized with indexing and replication
- **Caching**: Can add Redis for session/cache management
- **Queue System**: Can add Celery for async task processing
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
