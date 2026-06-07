"""
Script to run database migrations
"""
import os
import subprocess

def run_migrations():
    """Run Alembic migrations"""
    print("Running database migrations...")
    
    # Initialize Alembic if not already initialized
    if not os.path.exists("migrations"):
        subprocess.run(["alembic", "init", "migrations"])
    
    # Run migrations
    subprocess.run(["alembic", "upgrade", "head"])
    
    print("Migrations completed!")

if __name__ == "__main__":
    run_migrations()
