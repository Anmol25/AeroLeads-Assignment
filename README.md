# AeroLeads AI/ML Developer Assignment

This repository contains three independent mini-projects built as part of the AeroLeads AI/ML Developer role assignment. Each project demonstrates practical application of Python for automation, AI content generation, and telephony workflow.

> To run or explore any app in detail, please refer to the README inside its own folder. (See the `LinkedIn-Scraping`, `Autodialer`, and `AI_Article_generate` subdirectories.)

## Projects Overview

### 1. LinkedIn-Scraping
Automates the collection of multiple LinkedIn profile details (e.g., names, titles, companies, locations) using Selenium-based browsing. Output is stored in `scraped_profiles/linkedin_data.csv`.

Key points:
- Headless or visible browser automation
- Persistent Chrome profile folder (`selenium_profile/`) to reduce repeated logins
- CSV export for downstream enrichment
- Emphasis on respectful, rate-limited scraping (avoid aggressive request patterns)

### 2. Autodialer
Enables automated outbound calling to a list of phone numbers and plays a predefined voice message. Useful for notification campaigns or lead qualification triggers.

Key points:
- Batch processing of phone contacts
- Logging of call attempts and results (`call_logs.py` / `logs.py`)
- Extensible agent abstraction in `src/agent.py` and callable tools in `src/tools.py`
- Designed for integration with telephony APIs (e.g., Twilio) — actual provider specifics may be configured inside the project (see its README)

### 3. AI Article Generator
Generates long-form blog-style articles from a user prompt or topic seed. Exposes a Streamlit interface for quick iteration and export.

Key points:
- Topic-to-structured outline expansion
- LLM-powered paragraph generation (see `agent.py`)
- Optionally supports refinement loops before finalizing output
- Suitable for marketing content or SEO drafts

## Repository Structure (High-Level)

```
.
├── README.md  # (You are here) Root overview
├── LinkedIn-Scraping/
│   ├── streamlit_app.py
│   ├── scrapper.py
│   ├── scraped_profiles/
│   └── selenium_profile/
├── Autodialer/
│   ├── streamlit_app.py
│   ├── call_logs.py
│   ├── src/
│   │   ├── agent.py
│   │   ├── tools.py
│   │   └── logs.py
└── AI_Article_generate/
	├── streamlit_app.py
	├── blogs.py
	├── src/
	│   └── agent.py
	└── main.py
```

## Tech & Dependencies

All three projects are Python-based. Each subfolder includes its own `requirements.txt` tailored to its domain (automation, telephony integration, or LLM/article generation). Common likely libraries:
- Streamlit (UI front-end)
- Selenium (LinkedIn scraping)
- Requests / HTTP utilities
- LLM / AI provider SDKs (depending on configuration in `agent.py`)

Install dependencies per project rather than at the root for isolation.

## Quick Start (Per Project)

1. Clone the repository:
```bash
git clone https://github.com/Anmol25/AeroLeads-Assignment.git
cd AeroLeads-Assignment
```
2. Enter a project folder, e.g. LinkedIn scraping:
```bash
cd LinkedIn-Scraping
```
3. Create & activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate
```
4. Install its dependencies:
```bash
pip install -r requirements.txt
```
5. Run the Streamlit app (where provided):
```bash
streamlit run streamlit_app.py
```

Repeat equivalent steps inside `Autodialer/` and `AI_Article_generate/` folders. Consult each folder's README for provider keys, environment variables, or additional setup.


## Ethical & Compliance Notes
- Respect LinkedIn Terms of Service and local data privacy regulations (e.g., GDPR). Use scraping only on publicly available data and for legitimate business purposes.
- Ensure you have consent or a lawful basis for placing automated voice calls.
- AI-generated content should be reviewed for factual accuracy before publication.

## Extensibility Ideas
- Add scheduling (cron / task queue) for periodic scraping or calling.
- Integrate vector search for article topic enrichment.
- Add sentiment or entity extraction pass on scraped profile summaries.
- Implement retry/backoff logic for telephony API failures.

## Troubleshooting
| Issue | Possible Cause | Suggested Fix |
|-------|----------------|---------------|
| Browser fails to start | Chromedriver version mismatch | Update chromedriver in `LinkedIn-Scraping/chromedriver-linux64/` |
| Empty CSV output | Selectors changed on LinkedIn | Adjust locators in `scrapper.py` |
| Call API errors | Missing/invalid credentials | Check environment variables in Autodialer README |
| Slow article generation | Large prompt / model latency | Reduce topic scope or optimize agent parameters |


## Attribution
Developed for the AeroLeads AI/ML Developer assignment by Anmol.

---
For implementation or run details: please open the README inside each project folder.
