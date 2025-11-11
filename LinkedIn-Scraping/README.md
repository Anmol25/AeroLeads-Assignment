## LinkedIn Profile Scraper (Streamlit + Selenium)

A simple Streamlit app that logs into LinkedIn using credentials from a `.env` file and scrapes public details from one or more profile URLs that you provide as a comma‑separated list. Results are displayed in the app and saved to a CSV for reuse.

> Important: Use this project responsibly and in accordance with LinkedIn’s Terms of Service and applicable laws. This is intended for personal/educational use.

---

## What it does

- Logs into LinkedIn with your credentials (read from environment variables).
- Accepts one or more LinkedIn profile URLs, comma separated, via the Streamlit UI.
- Scrapes key profile sections such as Name, Headline, Company, Location, About, and selected sections (Experience, Education, Skills, etc.).
- Displays a table in the app and saves results to `scraped_profiles/linkedin_data.csv`.

### Supported sections

These sections are saved as JSON strings per profile row in the CSV to keep the file tabular:
- Experience
- Education
- Licenses & certifications
- Projects
- Skills
- Publications
- Courses
- Honors & awards
- Languages

---

## Prerequisites

- Python 3.10+ (3.12 works too)
- Google Chrome or Chromium installed
- A matching ChromeDriver
	- This repo ships with a Linux ChromeDriver at `./chromedriver-linux64/chromedriver`.
	- If Chrome updates and versions mismatch, download a compatible driver and update the path in `src/scrapper.py` if needed.

---

## Setup

1) Clone the repo and create a virtual environment (recommended)

```bash
git clone <this-repo-url>
cd LinkedIn-Scraping
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Configure environment variables

Create a file named `.env` in the project root (or copy from `.env.example`) with your LinkedIn credentials:

```env
LINKEDIN_ID=your_email@example.com
LINKEDIN_PASS=your_linkedin_password
```

Notes
- Never commit real credentials to source control. The provided `.gitignore` excludes `.env`.
- If you have multi‑factor authentication, the app will pause to let you complete any CAPTCHA/MFA challenges in the browser window.

4) Ensure ChromeDriver is executable (Linux)

```bash
chmod +x ./chromedriver-linux64/chromedriver
```

---

## Run the app

```bash
streamlit run streamlit_app.py
```

Open the URL that Streamlit prints (typically http://localhost:8501).

---

## Usage

1) In the text area, paste LinkedIn profile URLs separated by commas.
	 - Example:
		 ```
		 https://www.linkedin.com/in/john-doe/, https://www.linkedin.com/in/jane-smith/
		 ```
	 - The app validates that each URL begins with `https://www.linkedin.com/in/`.
2) Click “Scrape Profiles”.
3) A Chrome window will open. If prompted, complete any CAPTCHA/MFA. The app waits briefly during login for you to finish.
4) When done, results are:
	 - Shown in the Streamlit table.
	 - Saved to `scraped_profiles/linkedin_data.csv`.

Output columns include basic fields like `Name`, `Headline`, `Company`, `Location`, `About`, and JSON‑string columns for the sections listed above (e.g., `Experience`, `Education`, `Skills`, ...).

---

## How it works (high‑level)

- `src/scrapper.py` uses Selenium to:
	- Open Chrome with a persistent profile at `selenium_profile/` (keeps sessions/cookies across runs).
	- Navigate to LinkedIn login and fill `LINKEDIN_ID` / `LINKEDIN_PASS` from `.env`.
	- Visit each provided profile and extract key sections.
	- Write results to a DataFrame and append to `scraped_profiles/linkedin_data.csv`.
- `streamlit_app.py` provides the UI and basic URL validation.

---

## Project structure

```
.
├── chromedriver-linux64/           # Bundled ChromeDriver (Linux)
├── scraped_profiles/               # Output CSV will be written here
├── selenium_profile/               # Persistent Chrome profile for Selenium
├── src/
│   └── scrapper.py                 # Selenium scraper implementation
├── streamlit_app.py                # Streamlit UI
├── requirements.txt
└── README.md
```

---

## Troubleshooting

- CAPTCHA/MFA loops or login fails
	- Keep the browser window in focus and complete the challenge; the app waits for a short period after clicking Sign in.
	- If issues persist, close the app and delete the `selenium_profile/` folder to reset the session, then try again.

- Version mismatch: Chrome vs ChromeDriver
	- If Selenium cannot start or you see “this version of ChromeDriver only supports Chrome version …”, download the compatible driver and update the path in `src/scrapper.py`:
		```python
		self.chromedriver_path = "./chromedriver-linux64/chromedriver"
		```

- Empty/partial data
	- LinkedIn’s UI changes over time; selectors may need updates.
	- Some sections are not available on all profiles.

- Rate limiting or blocks
	- Avoid sending too many requests too quickly; throttle usage and scrape responsibly.

---

## Notes and safety

- Respect LinkedIn’s Terms of Service and robots policies.
- Only scrape data you’re authorized to access.
- Store credentials securely (environment variables, secret managers). Rotate credentials if they were ever committed by mistake.

---

## Tech stack

- Python, Selenium, ChromeDriver
- Streamlit for the UI
- pandas for table/CSV handling

