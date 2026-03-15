#!/usr/bin/env python3
"""SQLite database analysis plugin—chambers of secrets revealed."""

import sqlite3
import json
import os

class SqlitePlugin:
    @staticmethod
    def preview(db_file=None):
        """Preview contents of SQLite database."""
        try:
            if not db_file:
                # Find first .db file in uploads
                uploads_dir = os.path.join('vault', 'uploads')
                if os.path.exists(uploads_dir):
                    for f in os.listdir(uploads_dir):
                        if f.endswith('.db') or f.endswith('.sqlite'):
                            db_file = os.path.join(uploads_dir, f)
                            break
            
            if not db_file:
                return {"error": "No SQLite database found"}
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Get tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            preview = {}
            for table in tables[:5]:  # First 5 tables
                table_name = table[0]
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()
                preview[table_name] = [str(row) for row in rows]
            
            conn.close()
            return {"success": True, "preview": preview, "tables": len(tables)}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def schema(db_file=None):
        """Get database schema."""
        try:
            conn = sqlite3.connect(db_file or ':memory:')
            cursor = conn.cursor()
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
            schema = cursor.fetchall()
            conn.close()
            return {"schema": [row[0] for row in schema]}
        except Exception as e:
            return {"error": str(e)}

if __name__ != '__main__':
    from plugins.registry import register
    register('sqlite', SqlitePlugin)
