
from pathlib import Path
import sqlite3

absolute_path = Path(__file__).parent
notes_db = absolute_path / 'notes.db'

conn = sqlite3.connect(notes_db)
try:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        verified INTEGER NOT NULL DEFAULT 0)"""
    )
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes(
        notes_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL UNIQUE,
        body TEXT,
        archived INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (user_id))"""
    )
finally:
    conn.close()