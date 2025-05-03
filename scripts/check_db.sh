#!/bin/bash

# --- Configuration ---
# Adjust this path to the actual location of your SQLite database file
DB_PATH="../tennis_tournament.db" 
TABLE_NAME="tournaments"
# --- End Configuration ---

# Check if the database file exists
if [ ! -f "$DB_PATH" ]; then
    echo "Error: Database file not found at $DB_PATH"
    exit 1
fi

# Check if sqlite3 command is available
if ! command -v sqlite3 &> /dev/null; then
    echo "Error: sqlite3 command not found. Please install it."
    echo "On macOS: brew install sqlite"
    echo "On Debian/Ubuntu: sudo apt-get update && sudo apt-get install sqlite3"
    exit 1
fi

echo "Querying database: $DB_PATH"
echo "Table: $TABLE_NAME"
echo "---"

# Show table schema
echo "Table Schema:"
sqlite3 "$DB_PATH" <<EOF
.headers off
.mode list
PRAGMA table_info(${TABLE_NAME});
EOF

echo -e "\nAll Tables:"
# List tables using sqlite3
sqlite3 "$DB_PATH" <<EOF
.tables
EOF

echo -e "\nAll Tournament Records:"
# Show all records in the tournaments table
sqlite3 "$DB_PATH" <<EOF
.headers on
.mode column
SELECT * FROM ${TABLE_NAME};
EOF

echo "---"
echo "Query finished."

exit 0