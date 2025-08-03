import sqlite3
import os
import json
from datetime import datetime

class Database:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._initialize_tables()

    def _initialize_tables(self):
        cursor = self._connection.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'editor',
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Websites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS websites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                user_id INTEGER,
                business_type TEXT,
                industry TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Roles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                permissions TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        self._connection.commit()

    @property
    def connection(self):
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()

# Global database instance
db_instance = Database()
db = db_instance.connection

