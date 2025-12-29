# import sqlite3
# from datetime import datetime

# DB_NAME = "healthcare.db"

# def save_appointments(patient_name, doctor_name, appointment_datetime, status="Booked"):
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()

#     # ---------- USER ----------
#     cursor.execute("SELECT id FROM users WHERE username=?", (patient_name,))
#     user = cursor.fetchone()
#     if not user:
#         cursor.execute(
#             "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
#             (patient_name, "", 0)
#         )
#         user_id = cursor.lastrowid
#     else:
#         user_id = user[0]

#     # ---------- DOCTOR ----------
#     cursor.execute("SELECT id FROM doctors WHERE name=?", (doctor_name,))
#     doctor = cursor.fetchone()
#     if not doctor:
#         raise ValueError("Doctor does not exist")

#     doctor_id = doctor[0]

#     # ---------- DATETIME ----------
#     if isinstance(appointment_datetime, datetime):
#         appointment_datetime = appointment_datetime.strftime("%Y-%m-%d %H:%M:%S")

#     # ---------- APPOINTMENT ----------
#     cursor.execute("""
#         INSERT INTO appointments (user_id, doctor_id, appointment_datetime, status)
#         VALUES (?, ?, ?, ?)
#     """, (user_id, doctor_id, appointment_datetime, status))

#     conn.commit()
#     conn.close()


# save_appointments.py
# save_appointments.py
# save_appointments.py
import sqlite3
import os

DB = os.path.abspath("healthcare.db")

def get_connection():
    return sqlite3.connect(DB)

def save_appointments(patient_name, doctor_name, appointment_datetime, status):
    print("🔥🔥🔥 save_appointments CALLED 🔥🔥🔥")
    print("PATIENT:", patient_name)
    print("DOCTOR:", doctor_name)
    print("DATETIME:", appointment_datetime)
    print("STATUS:", status)
    print("DB PATH:", DB)

    try:
        with get_connection() as conn:
            c = conn.cursor()

            user_row = c.execute(
                "SELECT id FROM users WHERE username = ?",
                (patient_name,)
            ).fetchone()
            print("USER ROW:", user_row)

            doctor_row = c.execute(
                "SELECT id FROM doctors WHERE name LIKE ?",
                (f"%{doctor_name.replace('Dr.', '').strip()}%",)
            ).fetchone()
            print("DOCTOR ROW:", doctor_row)

            if not user_row or not doctor_row:
                print("❌ USER OR DOCTOR NOT FOUND — NOT SAVING")
                return

            c.execute("""
                INSERT INTO appointments (user_id, doctor_id, appointment_datetime, status)
                VALUES (?, ?, ?, ?)
            """, (user_row[0], doctor_row[0], appointment_datetime, status))

            conn.commit()
            print("✅✅✅ APPOINTMENT SAVED SUCCESSFULLY")

    except Exception as e:
        print("❌❌❌ ERROR:", e)
