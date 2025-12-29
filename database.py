# database.py
import sqlite3

DB = "doctors.db"

def init_db():
    """Initialize the main database and create tables."""
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Doctors table
    c.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL
    )
    """)

    # Patient history table
    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        symptoms TEXT,
        diagnosis TEXT,
        doctor_id INTEGER,
        date TEXT,
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT,
       specialty TEXT,
       bio TEXT,
       working_days TEXT,
       timings TEXT,
       hospital TEXT,
       location TEXT
)
""")


    conn.commit()
    conn.close()
