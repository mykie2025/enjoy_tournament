#!/usr/bin/env python
"""
Setup and Run script for the Tennis Tournament Analysis System
This script handles database initialization and running the FastAPI server
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def setup_database():
    """Initialize the database with tables and sample data"""
    print("Setting up the database...")
    
    # Import necessary modules
    from backend.database.database import engine, Base
    from backend.database.models import User, Tournament, Match, Point, Analysis, Recommendation, UserPreference
    
    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Import and run database initialization
    from backend.database.init_db import init_database
    init_database()
    
    print("Database setup complete!")

def run_server():
    """Run the FastAPI server"""
    print("Starting the FastAPI server...")
    
    # Use subprocess to run uvicorn with the correct module path
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "backend.app.main:app", 
        "--host", os.getenv("API_HOST", "localhost"),
        "--port", os.getenv("API_PORT", "8000"),
        "--reload"
    ])

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tennis Tournament Analysis System")
    parser.add_argument("--setup-db", action="store_true", help="Set up the database")
    parser.add_argument("--run", action="store_true", help="Run the FastAPI server")
    
    args = parser.parse_args()
    
    if args.setup_db:
        setup_database()
    
    if args.run or not (args.setup_db or args.run):
        run_server()
