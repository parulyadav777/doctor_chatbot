# ai_booking.py
import json
from datetime import datetime, timedelta
from backend import chat_with_model, get_doctor_by_specialty, book_appointment

SYSTEM_PROMPT = """
You are a helpful AI health assistant.
If the user wants to book an appointment, respond ONLY in JSON like:
{
  "action": "book_appointment",
  "doctor_specialty": "Cardiologist",
  "date": "YYYY-MM-DD or empty",
  "time": "HH:MM or empty"
}
If date or time is missing, leave it empty.
"""

def get_default_datetime():
    """Next day at 10:00 AM"""
    next_day = datetime.now() + timedelta(days=1)
    return next_day.strftime("%Y-%m-%d"), "10:00"

def handle_user_message(user_input, user_id):
    """
    Handles user input for medical queries and appointment booking.
    Returns AI response or confirmation of booked appointment.
    """
    # Ask AI model via backend
    response = chat_with_model(f"{SYSTEM_PROMPT}\nUser: {user_input}")

    # Clean AI response
    clean = response.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(clean)

        if data.get("action") == "book_appointment":
            specialty = data.get("doctor_specialty")
            date = data.get("date")
            time = data.get("time")

            # If AI didn't provide date/time, use default
            if not date or not time:
                date, time = get_default_datetime()

            # Fetch doctor info
            doctors = get_doctor_by_specialty(specialty)
            if not doctors:
                return f"❌ No doctor found for {specialty}"

            # Take first doctor
            doctor_id, doctor_name = doctors[0][0], doctors[0][1]
            appointment_datetime = f"{date} {time}"

            # Book appointment in backend DB
            book_appointment(user_id, doctor_id, appointment_datetime)

            return f"✅ Appointment booked with {doctor_name} on {date} at {time}"

        # For other AI responses, just return text
        return clean

    except json.JSONDecodeError:
        # If AI response is not valid JSON, just return text
        return clean
