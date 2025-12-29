import sqlite3
import os

# Use correct relative path
DBs = ["healthcare.db", "database.db"]

for db in DBs:
    db_path = os.path.join(os.getcwd(), db)  # ensures full path
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Check table exists before deleting
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='appointments'")
    if cur.fetchone():
        cur.execute("DELETE FROM appointments;")
        conn.commit()
        print(f"✅ Appointments cleared in {db}")
    else:
        print(f"⏭ No appointments table in {db}")

    conn.close()
