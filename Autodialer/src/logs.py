from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")


def fetch_call_logs():
    """Fetch call logs from Twilio account.
    Returns:
        list: A list of call log dictionaries.
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    calls = client.calls.list(limit=50)  # Fetch last 50 call logs
    call_logs = []
    for record in calls:
        call_logs.append({
            "sid": record.sid,
            "to": record.to,
            "status": record.status,
            "start_time": record.start_time,
            "end_time": record.end_time,
            "duration": record.duration
        })
    return call_logs
