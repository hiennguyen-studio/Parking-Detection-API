<<<<<<< HEAD
# Project Structure Documentation

## Directory Layout

```
.
├── src/                                  # Source code
│   ├── __init__.py
│   ├── AI/                              # AI/ML models and detection logic
│   │   ├── __init__.py
│   │   ├── detector.py
│   │   └── model_manager.py
│   │
│   ├── camera/                          # Camera/video stream handling
│   │   ├── __init__.py
│   │   ├── camera_handler.py
│   │   └── stream_processor.py
│   │
│   ├── user/                            # User management and authentication
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user_manager.py
│   │
│   ├── notify/                          # Notification service
│   │   ├── __init__.py
│   │   ├── telegram_bot.py              # Telegram notification
│   │   ├── email_service.py
│   │   └── notification_manager.py
│   │
│   ├── backend/                         # REST API and application logic
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI entry point
│   │   ├── api/                         # API routes
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── violations.py
│   │   │   │   ├── cameras.py
│   │   │   │   ├── users.py
│   │   │   │   └── statistics.py
│   │   │   └── schemas/
│   │   │       ├── __init__.py
│   │   │       ├── violation.py
│   │   │       ├── camera.py
│   │   │       └── user.py
│   │   │
│   │   └── dashboard/                  # Web dashboard
│   │       ├── __init__.py
│   │       ├── templates/               # HTML templates
│   │       │   ├── base.html
│   │       │   ├── index.html
│   │       │   ├── violations.html
│   │       │   └── statistics.html
│   │       └── static/                  # CSS, JS files
│   │           ├── css/
│   │           │   └── style.css
│   │           └── js/
│   │               └── dashboard.js
│   │
│   ├── database/                        # Database models and queries
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── db_manager.py
│   │   └── schemas.py
│   │
│   ├── config/                          # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py                  # Main settings
│   │   ├── telegram_config.py           # Telegram configuration
│   │   └── logging_config.py
│   │
│   └── utils/                           # Utility functions
│       ├── __init__.py
│       ├── helpers.py
│       └── validators.py
│
├── tests/                               # Unit and integration tests
│   ├── __init__.py
│   ├── AI/
│   │   ├── __init__.py
│   │   └── test_detector.py
│   ├── camera/
│   │   ├── __init__.py
│   │   └── test_camera_handler.py
│   ├── user/
│   │   ├── __init__.py
│   │   └── test_auth.py
│   ├── notify/
│   │   ├── __init__.py
│   │   └── test_telegram_bot.py
│   ├── backend/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── database/
│       ├── __init__.py
│       └── test_models.py
│
├── migrations/                          # Database migrations (Alembic)
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── data/                                # Data storage
│   ├── videos/                          # Input video files
│   ├── images/                          # Processed/captured images
│   ├── evidence/                        # Evidence files (violation records)
│   └── models/                          # Pre-trained AI models
│
├── docker/                              # Docker configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
├── .github/                             # GitHub workflows
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── docs/                                # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   └── TELEGRAM_BOT.md
│
├── scripts/                             # Utility scripts
│   ├── setup_db.py
│   ├── migrate_db.py
│   └── init_data.py
│
├── logs/                                # Application logs
│
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment variables template
├── .gitignore                           # Git ignore rules
├── pytest.ini                           # Pytest configuration
├── Dockerfile                           # Docker setup
├── docker-compose.yml                   # Docker compose
├── README.md                            # Project overview
└── PROJECT_STRUCTURE.md                 # This file
```

## Directory Descriptions

### src/
**Core application source code**

- **AI/**: Machine learning models, prediction logic, and detection algorithms
- **camera/**: Video capture, stream processing, and frame extraction
- **user/**: User registration, authentication, and profile management
- **notify/**: Email, SMS, and push notification handlers
- **backend/**: REST API endpoints, business logic, and main application server
- **database/**: Data models, ORM setup, and database queries
- **utils/**: Helper functions, validators, and utility modules

### tests/
**Automated tests mirroring src/ structure**

Each module should have corresponding unit and integration tests. Use pytest or unittest.

### data/
**Data storage (non-code)**

- **videos/**: Raw video input files for processing
- **images/**: Captured frames and processed images
- **evidence/**: Violation records with timestamps and metadata
- **models/**: Pre-trained AI models (.pth, .h5, .pkl files)

### docs/
**Project documentation**

- API documentation
- Installation guides
- Architecture diagrams
- User guides

### config/
**Configuration files**

- Database configuration
- API settings
- Model paths and parameters
- Logging configuration

### scripts/
**Utility and automation scripts**

- Database migration scripts
- Data processing scripts
- Setup and initialization scripts

### logs/
**Application runtime logs**

- API server logs
- AI model execution logs
- Error and debug logs

## Recommendations for This Structure

✅ **Strengths:**
1. Clear separation of concerns
2. Modular design - easy to test and maintain
3. Dedicated test directory mirroring src structure
4. Organized data storage
5. Good documentation structure

⚠️ **Suggestions for Improvement:**

1. **Add `src/__init__.py`** - Make src a proper Python package
2. **Add module `__init__.py` files** - Each folder should have `__init__.py`
3. **Consider adding `src/config/`** - Move configuration to source control (with .env for secrets)
4. **Add `src/models/`** - Separate database models from the database module
5. **Consider `docker/` folder** - For Docker configuration if containerizing
6. **Add `Dockerfile` and `docker-compose.yml`** - For containerization
7. **Consider `migrations/` folder** - For database schema migrations
8. **Add `.github/` folder** - For CI/CD workflows

## Usage Notes

- Keep `data/` directory in `.gitignore` for large files
- Store secrets in `.env` file (never commit)
- Use `config/` folder for non-secret configuration files
- Place database migrations in a dedicated folder
- Organize tests to match src structure exactly
=======
# Project Structure Documentation

## Directory Layout

```
.
├── src/                                  # Source code
│   ├── __init__.py
│   ├── AI/                              # AI/ML models and detection logic
│   │   ├── __init__.py
│   │   ├── detector.py
│   │   └── model_manager.py
│   │
│   ├── camera/                          # Camera/video stream handling
│   │   ├── __init__.py
│   │   ├── camera_handler.py
│   │   └── stream_processor.py
│   │
│   ├── user/                            # User management and authentication
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user_manager.py
│   │
│   ├── notify/                          # Notification service
│   │   ├── __init__.py
│   │   ├── telegram_bot.py              # Telegram notification
│   │   ├── email_service.py
│   │   └── notification_manager.py
│   │
│   ├── backend/                         # REST API and application logic
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI entry point
│   │   ├── api/                         # API routes
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── violations.py
│   │   │   │   ├── cameras.py
│   │   │   │   ├── users.py
│   │   │   │   └── statistics.py
│   │   │   └── schemas/
│   │   │       ├── __init__.py
│   │   │       ├── violation.py
│   │   │       ├── camera.py
│   │   │       └── user.py
│   │   │
│   │   └── dashboard/                  # Web dashboard
│   │       ├── __init__.py
│   │       ├── templates/               # HTML templates
│   │       │   ├── base.html
│   │       │   ├── index.html
│   │       │   ├── violations.html
│   │       │   └── statistics.html
│   │       └── static/                  # CSS, JS files
│   │           ├── css/
│   │           │   └── style.css
│   │           └── js/
│   │               └── dashboard.js
│   │
│   ├── database/                        # Database models and queries
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── db_manager.py
│   │   └── schemas.py
│   │
│   ├── config/                          # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py                  # Main settings
│   │   ├── telegram_config.py           # Telegram configuration
│   │   └── logging_config.py
│   │
│   └── utils/                           # Utility functions
│       ├── __init__.py
│       ├── helpers.py
│       └── validators.py
│
├── tests/                               # Unit and integration tests
│   ├── __init__.py
│   ├── AI/
│   │   ├── __init__.py
│   │   └── test_detector.py
│   ├── camera/
│   │   ├── __init__.py
│   │   └── test_camera_handler.py
│   ├── user/
│   │   ├── __init__.py
│   │   └── test_auth.py
│   ├── notify/
│   │   ├── __init__.py
│   │   └── test_telegram_bot.py
│   ├── backend/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── database/
│       ├── __init__.py
│       └── test_models.py
│
├── migrations/                          # Database migrations (Alembic)
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── data/                                # Data storage
│   ├── videos/                          # Input video files
│   ├── images/                          # Processed/captured images
│   ├── evidence/                        # Evidence files (violation records)
│   └── models/                          # Pre-trained AI models
│
├── docker/                              # Docker configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
├── .github/                             # GitHub workflows
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── docs/                                # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   └── TELEGRAM_BOT.md
│
├── scripts/                             # Utility scripts
│   ├── setup_db.py
│   ├── migrate_db.py
│   └── init_data.py
│
├── logs/                                # Application logs
│
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment variables template
├── .gitignore                           # Git ignore rules
├── pytest.ini                           # Pytest configuration
├── Dockerfile                           # Docker setup
├── docker-compose.yml                   # Docker compose
├── README.md                            # Project overview
└── PROJECT_STRUCTURE.md                 # This file
```

## Directory Descriptions

### src/
**Core application source code**

- **AI/**: Machine learning models, prediction logic, and detection algorithms
- **camera/**: Video capture, stream processing, and frame extraction
- **user/**: User registration, authentication, and profile management
- **notify/**: Email, SMS, and push notification handlers
- **backend/**: REST API endpoints, business logic, and main application server
- **database/**: Data models, ORM setup, and database queries
- **utils/**: Helper functions, validators, and utility modules

### tests/
**Automated tests mirroring src/ structure**

Each module should have corresponding unit and integration tests. Use pytest or unittest.

### data/
**Data storage (non-code)**

- **videos/**: Raw video input files for processing
- **images/**: Captured frames and processed images
- **evidence/**: Violation records with timestamps and metadata
- **models/**: Pre-trained AI models (.pth, .h5, .pkl files)

### docs/
**Project documentation**

- API documentation
- Installation guides
- Architecture diagrams
- User guides

### config/
**Configuration files**

- Database configuration
- API settings
- Model paths and parameters
- Logging configuration

### scripts/
**Utility and automation scripts**

- Database migration scripts
- Data processing scripts
- Setup and initialization scripts

### logs/
**Application runtime logs**

- API server logs
- AI model execution logs
- Error and debug logs

## Recommendations for This Structure

✅ **Strengths:**
1. Clear separation of concerns
2. Modular design - easy to test and maintain
3. Dedicated test directory mirroring src structure
4. Organized data storage
5. Good documentation structure

⚠️ **Suggestions for Improvement:**

1. **Add `src/__init__.py`** - Make src a proper Python package
2. **Add module `__init__.py` files** - Each folder should have `__init__.py`
3. **Consider adding `src/config/`** - Move configuration to source control (with .env for secrets)
4. **Add `src/models/`** - Separate database models from the database module
5. **Consider `docker/` folder** - For Docker configuration if containerizing
6. **Add `Dockerfile` and `docker-compose.yml`** - For containerization
7. **Consider `migrations/` folder** - For database schema migrations
8. **Add `.github/` folder** - For CI/CD workflows

## Usage Notes

- Keep `data/` directory in `.gitignore` for large files
- Store secrets in `.env` file (never commit)
- Use `config/` folder for non-secret configuration files
- Place database migrations in a dedicated folder
- Organize tests to match src structure exactly
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
