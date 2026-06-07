<<<<<<< HEAD
"""
Script to initialize sample data
"""
from src.database.db_manager import DatabaseManager
from src.database.models import User, Camera
from src.config.settings import settings

def init_sample_data():
    """Create sample data"""
    print("Creating sample data...")
    
    db_manager = DatabaseManager(settings.DATABASE_URL)
    session = db_manager.get_session()
    
    try:
        # Create sample user
        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password="hashed_password"
        )
        session.add(user)
        
        # Create sample cameras
        cameras = [
            Camera(name="Camera 1", location="Intersection A", stream_url="rtsp://camera1.local"),
            Camera(name="Camera 2", location="Intersection B", stream_url="rtsp://camera2.local"),
            Camera(name="Camera 3", location="Parking Lot C", stream_url="rtsp://camera3.local"),
        ]
        session.add_all(cameras)
        
        session.commit()
        print("Sample data created successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error creating sample data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_sample_data()
=======
"""
Script to initialize sample data
"""
from src.database.db_manager import DatabaseManager
from src.database.models import User, Camera
from src.config.settings import settings

def init_sample_data():
    """Create sample data"""
    print("Creating sample data...")
    
    db_manager = DatabaseManager(settings.DATABASE_URL)
    session = db_manager.get_session()
    
    try:
        # Create sample user
        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password="hashed_password"
        )
        session.add(user)
        
        # Create sample cameras
        cameras = [
            Camera(name="Camera 1", location="Intersection A", stream_url="rtsp://camera1.local"),
            Camera(name="Camera 2", location="Intersection B", stream_url="rtsp://camera2.local"),
            Camera(name="Camera 3", location="Parking Lot C", stream_url="rtsp://camera3.local"),
        ]
        session.add_all(cameras)
        
        session.commit()
        print("Sample data created successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error creating sample data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_sample_data()
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
