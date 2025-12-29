####Backend.py
import os
import json
import sqlite3
import hashlib
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# ================= ENV =================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENROUTER_API_KEY missing")

DEFAULT_MODEL ="mistralai/mistral-7b-instruct:free"
print("OPENROUTER KEY LOADED:", OPENAI_API_KEY[:10], "...")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
    # api_key="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"
)

# ================= DB ===================
DB = "healthcare.db"

def get_connection():
    return sqlite3.connect(DB)

# def init_db():
#     """Initialize database with required tables."""
#     with get_connection() as conn:
#         c = conn.cursor()
#         # Users table
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS users(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE,
#                 password_hash TEXT,
#                 is_admin INTEGER DEFAULT 0
#             )
#         """)
#         # Chat sessions table
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS chat_sessions(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_id INTEGER,
#                 title TEXT,
#                 messages_json TEXT,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         # Doctors table
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS doctors(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT,
#                 specialty TEXT,
#                 bio TEXT,
#                 working_days TEXT,
#                 timings TEXT,
#                 hospital TEXT,
#                 location TEXT
#             )
#         """)
#         # Sample doctors (only insert if table empty)
       
#     c.executemany("""
# INSERT INTO doctors (name, specialty, bio, working_days, timings, hospital, location)
# VALUES (?, ?, ?, ?, ?, ?, ?)
# """, [
#     ("Dr. Arjun Mehta", "Cardiologist", "Heart specialist with 15 years experience", "Mon-Sat", "10 AM - 4 PM", "City Heart Hospital", "Mumbai"),
#     ("Dr. Kavita Rao", "Dermatologist", "Skin specialist", "Tue-Sun", "11 AM - 5 PM", "Skin Glow Clinic", "Delhi"),
#     ("Dr. Kabir Sharma", "Orthopedics", "Bone & Joint surgeon", "Mon-Fri", "9 AM - 2 PM", "Ortho Care Hospital", "Pune"),
#     ("Dr. Sophia Nair", "Pediatrics", "Child specialist", "Mon-Fri", "10 AM - 3 PM", "Child Health Clinic", "Bangalore"),
#     ("Dr. Raj Malhotra", "Neurologist", "Expert in migraine and epilepsy treatment", "Tue-Sat", "9 AM - 3 PM", "Brain Care Hospital", "Chennai"),
#     ("Dr. Ananya Singh", "Gynecologist", "Women health & maternity specialist", "Mon-Fri", "10 AM - 4 PM", "City Women's Clinic", "Delhi"),
#     ("Dr. Rohan Desai", "Gastroenterologist", "Digestive system expert", "Wed-Sun", "11 AM - 5 PM", "Gut Health Clinic", "Mumbai"),
#     ("Dr. Aarav Iyer", "ENT Specialist", "Ear, nose, and throat specialist", "Mon-Fri", "9 AM - 2 PM", "ENT Care Hospital", "Bangalore"),
#     ("Dr. Vikram Choudhary", "Pulmonologist", "Lung and respiratory expert", "Tue-Sat", "10 AM - 4 PM", "Lung Care Hospital", "Pune"),
#     ("Dr. Nisha Verma", "Endocrinologist", "Diabetes and hormone specialist", "Mon-Thu", "9 AM - 3 PM", "Endo Clinic", "Delhi"),
#     ("Dr. Sameer Kapoor", "Psychiatrist", "Mental health and counseling", "Tue-Fri", "11 AM - 5 PM", "Mind Care Clinic", "Mumbai"),
#     ("Dr. Priya Menon", "Ophthalmologist", "Eye specialist and surgeries", "Mon-Fri", "9 AM - 3 PM", "Vision Hospital", "Chennai"),
#     ("Dr. Aditya Shah", "Nephrologist", "Kidney specialist", "Wed-Sun", "10 AM - 4 PM", "Kidney Care Hospital", "Bangalore"),
#     ("Dr. Sneha Patil", "Rheumatologist", "Joint and autoimmune diseases", "Mon-Fri", "10 AM - 4 PM", "Joint Care Clinic", "Pune"),
#     ("Dr. Karan Gupta", "Oncologist", "Cancer specialist", "Tue-Sat", "9 AM - 3 PM", "Hope Cancer Center", "Delhi"),
#     ("Dr. Priya Sharma", "General Physician", "Experienced family doctor for adults and children", "Mon-Fri", "10 AM - 4 PM", "Wellness Health Center", "Delhi")
# ])
# # Appointments table
#     c.execute("""
#             CREATE TABLE IF NOT EXISTS appointments(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_id INTEGER,
#                 doctor_id INTEGER,
#                 appointment_datetime TEXT,
#                 status TEXT DEFAULT 'Booked'
#             )
#         """)
#     conn.commit()

def init_db():
    with get_connection() as conn:
        c = conn.cursor()

        # USERS
        c.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                is_admin INTEGER DEFAULT 0
            )
        """)

        # CHAT SESSIONS
        c.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                messages_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # DOCTORS
        c.execute("""
            CREATE TABLE IF NOT EXISTS doctors(
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

        # APPOINTMENTS
        c.execute("""
            CREATE TABLE IF NOT EXISTS appointments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                doctor_id INTEGER,
                appointment_datetime TEXT,
                status TEXT DEFAULT 'Booked'
            )
        """)

        # INSERT DOCTORS ONLY ONCE
        c.execute("SELECT COUNT(*) FROM doctors")
        if c.fetchone()[0] == 0:
            c.executemany("""
                INSERT INTO doctors
                (name, specialty, bio, working_days, timings, hospital, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                ("Dr. Arjun Mehta", "Cardiologist", "Heart specialist with 15 years experience", "Mon-Sat", "10 AM - 4 PM", "City Heart Hospital", "Mumbai"),
                ("Dr. Kavita Rao", "Dermatologist", "Skin specialist", "Tue-Sun", "11 AM - 5 PM", "Skin Glow Clinic", "Delhi"),
                ("Dr. Kabir Sharma", "Orthopedics", "Bone & Joint surgeon", "Mon-Fri", "9 AM - 2 PM", "Ortho Care Hospital", "Pune"),
                ("Dr. Sophia Nair", "Pediatrics", "Child specialist", "Mon-Fri", "10 AM - 3 PM", "Child Health Clinic", "Bangalore"),
                ("Dr. Raj Malhotra", "Neurologist", "Expert in migraine and epilepsy treatment", "Tue-Sat", "9 AM - 3 PM", "Brain Care Hospital", "Chennai"),
                ("Dr. Ananya Singh", "Gynecologist", "Women health & maternity specialist", "Mon-Fri", "10 AM - 4 PM", "City Women's Clinic", "Delhi"),
                ("Dr. Rohan Desai", "Gastroenterologist", "Digestive system expert", "Wed-Sun", "11 AM - 5 PM", "Gut Health Clinic", "Mumbai"),
                ("Dr. Aarav Iyer", "ENT Specialist", "Ear, nose, and throat specialist", "Mon-Fri", "9 AM - 2 PM", "ENT Care Hospital", "Bangalore"),
                ("Dr. Vikram Choudhary", "Pulmonologist", "Lung and respiratory expert", "Tue-Sat", "10 AM - 4 PM", "Lung Care Hospital", "Pune"),
                ("Dr. Nisha Verma", "Endocrinologist", "Diabetes and hormone specialist", "Mon-Thu", "9 AM - 3 PM", "Endo Clinic", "Delhi"),
                ("Dr. Sameer Kapoor", "Psychiatrist", "Mental health and counseling", "Tue-Fri", "11 AM - 5 PM", "Mind Care Clinic", "Mumbai"),
                ("Dr. Priya Menon", "Ophthalmologist", "Eye specialist and surgeries", "Mon-Fri", "9 AM - 3 PM", "Vision Hospital", "Chennai"),
                ("Dr. Aditya Shah", "Nephrologist", "Kidney specialist", "Wed-Sun", "10 AM - 4 PM", "Kidney Care Hospital", "Bangalore"),
                ("Dr. Sneha Patil", "Rheumatologist", "Joint and autoimmune diseases", "Mon-Fri", "10 AM - 4 PM", "Joint Care Clinic", "Pune"),
                ("Dr. Karan Gupta", "Oncologist", "Cancer specialist", "Tue-Sat", "9 AM - 3 PM", "Hope Cancer Center", "Delhi"),
                ("Dr. Priya Sharma", "General Physician", "Experienced family doctor", "Mon-Fri", "10 AM - 4 PM", "Wellness Health Center", "Delhi")
            ])

        conn.commit()


# Initialize DB on import
init_db()

# ================= AUTH =================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str) -> bool:
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users(username,password_hash) VALUES(?,?)",
                (username, hash_password(password))
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False
def authenticate_user(username: str, password: str) -> Optional[Dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, password_hash, is_admin FROM users WHERE username=?",
            (username,)
        ).fetchone()
    if row and hash_password(password) == row[1]:
        return {"id": row[0], "is_admin": row[2]}
    return None

# ================= CHAT STORAGE =================
def load_user_chat_sessions(user_id: int):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title FROM chat_sessions WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
    return rows

def load_chat_messages(chat_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT messages_json FROM chat_sessions WHERE id=?",
            (chat_id,)
        ).fetchone()
    return json.loads(row[0]) if row else []

def save_chat_session_with_messages(user_id: int, title: str, messages: list):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_sessions(user_id, title, messages_json) VALUES(?,?,?)",
            (user_id, title, json.dumps(messages))
        )
        conn.commit()
        return cur.lastrowid

def update_chat_session_messages(chat_id: int, messages: list):
    with get_connection() as conn:
        conn.execute(
            "UPDATE chat_sessions SET messages_json=? WHERE id=?",
            (json.dumps(messages), chat_id)
        )
        conn.commit()

# ================= DOCTOR FUNCTIONS =================
def get_all_doctors():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM doctors").fetchall()
    return rows

def get_doctor_by_specialty(specialty):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM doctors WHERE specialty LIKE ?", 
            (f"%{specialty}%",)
        ).fetchall()
    return rows

def create_doctor(name, specialty, bio, working_days, timings, hospital, location):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO doctors (name, specialty, bio, working_days, timings, hospital, location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, specialty, bio, working_days, timings, hospital, location))
        conn.commit()

# ================= APPOINTMENT FUNCTIONS =================
def book_appointment(user_id, doctor_id, appointment_datetime):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM appointments
        WHERE user_id=? AND doctor_id=? AND appointment_datetime=?
    """, (user_id, doctor_id, appointment_datetime))

    if cursor.fetchone():
        conn.close()
        return  # already booked

    cursor.execute("""
        INSERT INTO appointments (user_id, doctor_id, appointment_datetime, status)
        VALUES (?, ?, ?, 'Booked')
    """, (user_id, doctor_id, appointment_datetime))

    conn.commit()
    conn.close()
#def book_appointment(user_id, doctor_id, datetime_str):
 #   with get_connection() as conn:
  #      conn.execute(
   #         "INSERT INTO appointments (user_id, doctor_id, appointment_datetime) VALUES (?, ?, ?)",
     #       (user_id, doctor_id, datetime_str)
      #  )
       # conn.commit()

def cancel_appointment(app_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM appointments WHERE id = ?", (app_id,))
        conn.commit()

def is_day_allowed(working_days: str, day_name: str) -> bool:
    days_map = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    day_name = day_name.lower()[:3]

    if "-" in working_days:
        start, end = working_days.lower().split("-")
        start_i = days_map.index(start)
        end_i = days_map.index(end)
        return start_i <= days_map.index(day_name) <= end_i

    return day_name in working_days.lower()

def is_time_allowed(timings: str, time_str: str) -> bool:
    start_str, end_str = timings.split("-")
    start = datetime.strptime(start_str.strip(), "%I %p").time()
    end = datetime.strptime(end_str.strip(), "%I %p").time()
    user_time = datetime.strptime(time_str.strip(), "%I %p").time()
    return start <= user_time <= end

def validate_appointment(doctor_row, day_name, time_str):
    working_days = doctor_row[4]
    timings = doctor_row[5]

    if not is_day_allowed(working_days, day_name):
        return False, f"Doctor is not available on {day_name.title()}."

    if not is_time_allowed(timings, time_str):
        return False, f"Doctor is available only between {timings}."

    return True, "Slot available"

def load_user_appointments(user_id):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT a.id, d.name, d.specialty, a.appointment_datetime, a.status
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.user_id = ?
            ORDER BY a.appointment_datetime DESC
        """, (user_id,)).fetchall()
    return [{"id": r[0], "doctor_name": r[1], "specialty": r[2], "datetime": r[3], "status": r[4]} for r in rows]

# ================= AI =================
SYSTEM_PROMPT = """
You are a helpful, friendly AI health assistant.
You are not a doctor, but you can provide information on medicines, symptoms, general health advice, and over-the-counter treatments.
You do NOT diagnose diseases.
You only answer medical/health-related questions. 
If the user asks something unrelated to health or medicine, politely respond:
'I’m sorry, I can only provide medical-related information.'
Always use simple language and be conversational.
"""

def chat_with_model(user_input, chat_history=None, model=DEFAULT_MODEL):
    print("MODEL USED:", model)

    if not user_input or not user_input.strip():
        return "Please enter a medical-related question."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    if chat_history:
        messages.extend(chat_history[-10:])

    messages.append({"role": "user", "content": user_input})

    doctors = get_all_doctors()
    doctor_text = "\n".join([
        f"{d[1]} ({d[2]}) – {d[6]}, {d[7]}"
        for d in doctors
    ])

    messages.insert(
        1,
        {"role": "assistant", "content": f"Available Doctors:\n{doctor_text}"}
    )

    try:
        res = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=350
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


# ================= ALIASES =================
load_chat_sessions = load_user_chat_sessions
save_chat_session = save_chat_session_with_messages
update_chat_session = update_chat_session_messages


# ================= USERS (ADMIN) =================
def get_all_users():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, username, is_admin FROM users ORDER BY id ASC"
        ).fetchall()
    return rows