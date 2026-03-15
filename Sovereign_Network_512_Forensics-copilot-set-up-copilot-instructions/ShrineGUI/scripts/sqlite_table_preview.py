#!/usr/bin/env python3
"""SQLite table preview ritual—database chambers revealed."""

import sqlite3
import json
import os

try:
    # Look for .db files in vault/uploads
    db_files = []
    uploads_dir = os.path.join('vault', 'uploads')
    
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            if filename.endswith('.db') or filename.endswith('.sqlite'):
                db_files.append(os.path.join(uploads_dir, filename))
    
    if not db_files:
        print("No SQLite database relics found in vault/uploads")
        print("Expected: *.db or *.sqlite files")
    else:
        for db_path in db_files[:1]:  # Process first database
            print(f"SQLite preview: {os.path.basename(db_path)}")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # List tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if tables:
                for table in tables:
                    table_name = table[0]
                    print(f"\n  Table: {table_name}")
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    rows = cursor.fetchall()
                    for row in rows:
                        print(f"    {row}")
            else:
                print("  No tables found in this vessel")
            
            conn.close()

except ImportError:
    print("sqlite3 module not available (usually included with Python)")
except Exception as e:
    print(f"SQLite error: {e}")
