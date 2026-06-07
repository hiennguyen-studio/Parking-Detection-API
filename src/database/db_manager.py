<<<<<<< HEAD
"""
Database manager
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base


class DatabaseManager:
    """Manage database connections and operations"""

    def __init__(self, database_url: str):
        """Initialize database manager"""
        self.database_url = database_url
        self.engine = create_engine(database_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()

    def close(self):
        """Close database connection"""
        self.engine.dispose()
=======
"""
Database manager
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base


class DatabaseManager:
    """Manage database connections and operations"""

    def __init__(self, database_url: str):
        """Initialize database manager"""
        self.database_url = database_url
        self.engine = create_engine(database_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()

    def close(self):
        """Close database connection"""
        self.engine.dispose()
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
