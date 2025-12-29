import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ---------------- CHATS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    message TEXT,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ---------------- DOCTORS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    available_days TEXT
)
""")

# ---------------- APPOINTMENTS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    doctor_name TEXT,
    date TEXT,
    time TEXT,
    symptoms TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully")
