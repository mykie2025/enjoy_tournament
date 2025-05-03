"""
Migration script to add tournament selection fields to the Tournament model.
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add parent directory to path to import database module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.database.database import get_db_connection_string

def run_migration():
    """
    Add external_id, is_selected, and status fields to the tournaments table.
    """
    # Get database connection string
    db_path = get_db_connection_string().replace('sqlite:///', '')
    
    print(f"Running migration on database: {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(tournaments)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add external_id column if it doesn't exist
        if 'external_id' not in columns:
            print("Adding external_id column to tournaments table")
            cursor.execute("ALTER TABLE tournaments ADD COLUMN external_id TEXT")
        
        # Add is_selected column if it doesn't exist
        if 'is_selected' not in columns:
            print("Adding is_selected column to tournaments table")
            cursor.execute("ALTER TABLE tournaments ADD COLUMN is_selected BOOLEAN DEFAULT 0")
        
        # Add status column if it doesn't exist
        if 'status' not in columns:
            print("Adding status column to tournaments table")
            cursor.execute("ALTER TABLE tournaments ADD COLUMN status TEXT DEFAULT 'upcoming'")
        
        # Commit the changes
        conn.commit()
        print("Migration completed successfully")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
