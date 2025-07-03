import os
from datetime import timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
import dateparser

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

if not SERVICE_ACCOUNT_FILE:
    raise ValueError("Missing SERVICE_ACCOUNT_FILE in .env")

SCOPES = ["https://www.googleapis.com/auth/calendar"]
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("calendar", "v3", credentials=credentials)

def create_event_in_calendar(slots: dict) -> str:
    try:
        # 🔍 Step 1: Parse datetime using dateparser
        raw_datetime = f"{slots['date']} {slots['time']}"
        start_dt = dateparser.parse(raw_datetime)
        if start_dt is None:
            raise ValueError(f"Could not parse date/time: '{raw_datetime}'")

        # 🕒 Step 2: Parse duration
        duration_str = slots.get("duration", "30 minutes")
        duration_parts = duration_str.lower().split()
        duration_value = int(duration_parts[0])
        duration_unit = duration_parts[1]

        if "hour" in duration_unit:
            end_dt = start_dt + timedelta(hours=duration_value)
        elif "min" in duration_unit:
            end_dt = start_dt + timedelta(minutes=duration_value)
        else:
            raise ValueError(f"Unknown duration unit: {duration_unit}")

        # 📅 Step 3: Build the event
        event = {
            "summary": slots.get("purpose", "Meeting"),
            "location": slots.get("location", ""),
            "description": "Scheduled via AI agent",
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "attendees": [
                {"email": email.strip()}
                for email in slots.get("attendees", "").split(",") if email.strip()
            ],
            "reminders": {"useDefault": True},
        }

        created_event = service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event).execute()
        return created_event.get("htmlLink")

    except Exception as e:
        raise RuntimeError(f"Error creating event: {str(e)}")
