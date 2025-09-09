# db_logger.py
import sqlite3
import os
from datetime import datetime

DB_FILE = os.getenv("DB_FILE", "chat_logs.db")

# Create table if not exists
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            response TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Log one chat turn
def log_chat(user_id: str, message: str, response: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO chat_logs (user_id, message, response, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, message, response, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()
