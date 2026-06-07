# API Documentation

## Overview

The Parking Detection System API provides endpoints for managing cameras, violations, users, and retrieving statistics.

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Violations

#### List Violations
```
GET /violations
```

Query Parameters:
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 100)

Response:
```json
[
  {
    "id": 1,
    "camera_id": 1,
    "plate_number": "30A12345",
    "confidence": 0.95,
    "image_path": "/path/to/image.jpg",
    "is_confirmed": false,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### Get Violation
```
GET /violations/{violation_id}
```

#### Create Violation
```
POST /violations
```

Request Body:
```json
{
  "camera_id": 1,
  "plate_number": "30A12345",
  "confidence": 0.95,
  "image_path": "/path/to/image.jpg",
  "latitude": 21.0285,
  "longitude": 105.8542
}
```

### Cameras

#### List Cameras
```
GET /cameras
```

#### Get Camera
```
GET /cameras/{camera_id}
```

#### Create Camera
```
POST /cameras
```

Request Body:
```json
{
  "name": "Camera 1",
  "location": "Intersection A",
  "stream_url": "rtsp://camera.local"
}
```

### Users

#### List Users
```
GET /users
```

#### Get User
```
GET /users/{user_id}
```

#### Create User
```
POST /users
```

Request Body:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

### Statistics

#### Get Summary
```
GET /statistics/summary
```

Response:
```json
{
  "total_violations": 150,
  "violations_today": 12,
  "active_cameras": 3,
  "confirmed_violations": 145
}
```

#### Get Camera Statistics
```
GET /statistics/by-camera/{camera_id}
```

#### Get Daily Statistics
```
GET /statistics/by-date?date=2024-01-15
```

## Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Error Handling

All errors follow a standard format:

```json
{
  "detail": "Error message"
}
```

Common HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error
