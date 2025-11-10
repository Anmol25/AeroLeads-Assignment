from langchain.tools import tool
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")


@tool
def make_call(mobile_no: str, message: str):
    """Make a call to the given mobile number with the specified message.
    Args:
        mobile_no (str): The mobile number to call (in E.164 format, e.g., +1234567890).
        message (str): The message to be spoken during the call.
    Returns:
        str: The status of the call initiation.
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        call = client.calls.create(
            twiml=f"<Response><Say>{message}</Say></Response>",
            to=mobile_no,
            from_=TWILIO_NUMBER,
        )
        return f"Call initiated with SID: {call.sid}"
    except Exception as e:
        return f"Failed to make call with error as: {str(e)}"
