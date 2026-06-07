"""
Script to initialize database
"""
from src.database.db_manager import DatabaseManager
from src.config.settings import settings

def init_db():
    """Initialize database"""
    print(f"Initializing database at {settings.DATABASE_URL}...")
    
    db_manager = DatabaseManager(settings.DATABASE_URL)
    db_manager.init_db()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
