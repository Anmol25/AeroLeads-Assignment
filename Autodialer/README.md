# AutoDialer (Streamlit + Twilio + Gemini)

Call a verified phone number with a custom spoken message from a simple Streamlit app. The app uses a lightweight LangChain agent powered by Google Generative AI (Gemini) to validate the request and a Twilio tool to place the call. A Call Logs page shows the latest 50 calls from your Twilio account.

## Features

- Make a phone call to a verified number with a message that will be spoken to the recipient
- Enforce Twilio Trial restriction: only calls to the single verified number are allowed
- View the last 50 call records (SID, to, status, timestamps, duration)
- Simple two-page Streamlit UI: Home and Call Logs

## Requirements

- Python 3.10+ (recommended)
- A Twilio account (Trial is fine, but limited to verified numbers)
- A Google Generative AI (Gemini) API key

## Environment variables (.env)

Create a `.env` file in the project root with the following keys:

- `TWILIO_ACCOUNT_SID` — Your Twilio Account SID
- `TWILIO_AUTH_TOKEN` — Your Twilio Auth Token
- `TWILIO_NUMBER` — Your Twilio phone number in E.164 format, for example `+12025550123`
- `VERIFIED_NUMBER` — The destination phone number you verified in Twilio (E.164 format). The agent will only call this exact number while on a Trial account.
- `GOOGLE_API_KEY` — Gemini API key used by `langchain-google-genai`

Example `.env` (do not commit this file):

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_NUMBER=+12025550123
VERIFIED_NUMBER=+919876543210
GOOGLE_API_KEY= gemini-api-key
```

Notes:
- Twilio Trial accounts can only call verified numbers; make sure the number in `VERIFIED_NUMBER` is verified in your Twilio Console.
- Numbers must include the country code (E.164 format), e.g., `+1...`, `+91...`.

## Install and run

1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Create your `.env` file (see above)

4) Start the app

```bash
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

## Usage

Home page (`Home`):

- Enter a natural language instruction that includes the destination phone number (with country code) and the message to speak.
- Example prompts:
	- "Make a call to +919876543210 with the message: 'Hello, this is a test from AutoDialer.'"
	- "Call +12025550123 and say 'Your appointment is at 3 PM.'"
- Click "Make Call". The agent will:
	- Check that your input includes a phone number and that it matches `VERIFIED_NUMBER`.
	- If valid, place the call with Twilio and return the call SID.
	- If not valid, it will respond: "Due to the trial account of Twilio, I can make calls to verified numbers only."

Call Logs page (`Call Logs` or http://localhost:8501/call_logs):

- Shows the last 50 call records from your Twilio account.
- Click "Refresh" to reload the data.

## How it works

- UI: `streamlit_app.py` sets up two pages: `Home.py` and `call_logs.py`.
- Agent: `src/agent.py` creates a LangChain agent using `ChatGoogleGenerativeAI` (Gemini) and one tool.
- Tool: `src/tools.py` defines `make_call`, which uses the Twilio REST API to initiate a call and speak your message via TwiML `<Say>`.
- Logs: `src/logs.py` retrieves the last 50 calls using the Twilio API for display in the Call Logs page.

## Project structure

```
streamlit_app.py        # Page navigation
Home.py                 # Home page (enter instruction and trigger call)
call_logs.py            # Call Logs page (view recent 50 calls)
src/
	agent.py              # LangChain agent (Gemini) + system prompt + tool wiring
	tools.py              # Twilio "make_call" tool
	logs.py               # Fetch call logs from Twilio
requirements.txt        # Python dependencies
```

## Important limitations (Twilio Trial)

- Only calls to the single `VERIFIED_NUMBER` are allowed.
- The number must be in E.164 format and must match exactly what you set in `.env`.
- Audio is synthesized by Twilio's `<Say>`; long messages may be truncated or take longer to play.

## Troubleshooting

- ImportError: `from dotenv import load_dotenv`
	- The project pins `dotenv` in `requirements.txt`. If you still encounter import issues, install `python-dotenv`:
		```bash
		pip install python-dotenv
		```

- Calls fail or return an error string
	- Ensure all `.env` variables are set and correct.
	- Confirm `TWILIO_NUMBER` and `VERIFIED_NUMBER` are valid and in E.164 format.
	- For Trial, the call must be to the verified destination (`VERIFIED_NUMBER`).
	- Check Twilio Console for detailed call logs and errors.

- No output or page not found
	- Ensure Streamlit starts successfully and you are visiting http://localhost:8501.

## Security

- Keep your `.env` file private. It's already ignored by `.gitignore`.
- Rotate keys if you suspect they were exposed.

## Next steps / ideas

- Add a proper phone input field and message box with validation in the UI
- Support multiple verified destinations when the account is upgraded from Trial
- Add language/voice controls for Twilio TTS
- Persist call requests and outcomes to a database for auditability

---

Built with Streamlit, Twilio, and LangChain on Gemini.

