#book_appointments.py
import sqlite3
from datetime import datetime

DB_NAME = "healthcare.db"

def save_appointments(patient_name, doctor_name, appointment_datetime, status="pending"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # --- 1. Ensure user exists ---
    cursor.execute("SELECT id FROM users WHERE username=?", (patient_name,))
    user = cursor.fetchone()
    if not user:
        # Create user automatically
        cursor.execute("INSERT INTO users (username) VALUES (?)", (patient_name,))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE username=?", (patient_name,))
        user = cursor.fetchone()
        print(f"User '{patient_name}' was not found and has been created.")
    user_id = user[0]

    # --- 2. Ensure doctor exists ---
    cursor.execute("SELECT id FROM doctors WHERE name=?", (doctor_name,))
    doctor = cursor.fetchone()
    if not doctor:
        # Create doctor automatically
        cursor.execute("INSERT INTO doctors (name) VALUES (?)", (doctor_name,))
        conn.commit()
        cursor.execute("SELECT id FROM doctors WHERE name=?", (doctor_name,))
        doctor = cursor.fetchone()
        print(f"Doctor '{doctor_name}' was not found and has been created.")
    doctor_id = doctor[0]

    # --- 3. Ensure datetime is correct string ---
    if isinstance(appointment_datetime, datetime):
        appointment_datetime = appointment_datetime.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Saving appointment for {patient_name} with {doctor_name} at {appointment_datetime}")

    # --- 4. Insert appointment ---
    cursor.execute("""
        INSERT INTO appointments (user_id, doctor_id, appointment_datetime, status)
        VALUES (?, ?, ?, ?)
    """, (user_id, doctor_id, appointment_datetime, status))

    conn.commit()
    conn.close()
    print("Appointment saved successfully!")


