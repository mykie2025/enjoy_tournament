#!/usr/bin/env python
"""
Run script for the Tennis Tournament Analysis System
This script initializes the database and starts the FastAPI server
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

import uvicorn
from backend.database.database import engine, Base
from backend.database.models import User, Tournament, Match, Point, Analysis, Recommendation, UserPreference
import argparse

def init_db():
    """Initialize the database with tables and sample data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")
    
    # Import and run the database initialization
    from backend.database.init_db import init_database
    init_database()
    
    print("Database initialization complete!")

def run_server():
    """Run the FastAPI server"""
    print("Starting FastAPI server...")
    uvicorn.run(
        "backend.app.main:app", 
        host=os.getenv("API_HOST", "localhost"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tennis Tournament Analysis System")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database")
    parser.add_argument("--run-server", action="store_true", help="Run the FastAPI server")
    
    args = parser.parse_args()
    
    if args.init_db:
        init_db()
    
    if args.run_server or not (args.init_db or args.run_server):
        run_server()
