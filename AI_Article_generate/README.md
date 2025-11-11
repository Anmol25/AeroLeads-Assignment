AI Programming Article Generator (Streamlit)
=================================================

Generate polished, developer-focused programming articles from simple specifications using Google Gemini. Enter one or multiple article titles (optionally with notes like audience level, language, length, constraints) then navigate to the Blogs page to read the generated Markdown articles.

## ✨ Features

- Multiple article generation in a single request (one article per specification)
- Structured Markdown output: title, summary, table of contents, headings, code samples
- Supports audience & language tailoring (e.g., Beginner Rust, Intermediate Python)
- Uses Google Gemini (`gemini-2.5-flash`) with JSON schema enforcement for reliability
- Clean Streamlit UI with session-based persistence of generated articles
- Expandable blog cards for easy browsing

## 🧱 Architecture Overview

| Component | File | Purpose |
|-----------|------|---------|
| Streamlit entrypoint | `streamlit_app.py` | Declares navigation pages (Home, Blogs) |
| Home page | `main.py` | Text area for prompt + generation trigger; stores results in `st.session_state.blogs` |
| Blogs page | `blogs.py` | Renders generated articles (Markdown) in expandable sections |
| AI Agent | `src/agent.py` | Wraps Gemini client; applies system prompt & JSON schema to return structured articles |

Data models (Pydantic):
- `Article { title, content }`
- `ArticlesOutput { article_generated: bool, articles: List[Article] }`

Session state key: `blogs` (list of `Article` objects). After generation, navigate to Blogs page to view.

## 🛠 Requirements

| Dependency | Version (pinned) |
|------------|------------------|
| Python | 3.10+ (recommended) |
| streamlit | 1.51.0 |
| google-genai | 1.49.0 |
| python-dotenv | 0.9.9 |

## 🔐 Configuration (.env)

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Obtain an API key from Google AI Studio. Never commit `.env` to version control.

## 🚀 Quick Start

```bash
# 1. Clone repo
git clone <your-fork-or-repo-url>
cd AI_Article_generate

# 2. Create & activate virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your .env with GOOGLE_API_KEY
echo "GOOGLE_API_KEY=YOUR_KEY" > .env

# 5. Run the Streamlit app
streamlit run streamlit_app.py
```

Then:
1. Go to Home page (default).
2. Paste your article specifications into the text area.
3. Click "Generate Articles".
4. Navigate to Blogs page to read results.

## ✍️ Input Format Guidance

Enter one or more article specifications separated by line breaks or enumerated. Each should minimally include a title; optionally add audience, language, notes, length, constraints.

Example multi-article prompt:
```
Please generate three programming articles:

1) Title: "Getting Started with Rust"
	Audience: Beginner
	Notes: Focus on ownership & borrowing with simple code examples.

2) Title: "FastAPI Authentication Patterns"
	Audience: Intermediate
	Language: Python
	Notes: Include OAuth2, JWT, and pitfalls.

3) Title: "Scaling PostgreSQL Reads"
	Audience: Advanced
	Notes: Cover replication, connection pooling, monitoring.
```

## 📄 Output Structure (Per Article)

```
## <Title>
<1–2 sentence summary>
Table of Contents (with anchor links)
Body sections (##, ### headings)
Code blocks with language identifiers
Horizontal rule (---) between multiple articles
```

## 🔄 How Generation Works

1. `main.py` collects your raw specification text.
2. `ArticleGeneratorAgent.generate_articles()` sends it to Gemini with a strict system prompt.
3. Gemini returns JSON matching `ArticlesOutput` schema.
4. Articles are appended to `st.session_state.blogs`.
5. `blogs.py` renders each article's Markdown inside an expander.

If the prompt lacks any recognizable article specification, `article_generated` will be false and no articles are added.

## 🧪 Programmatic Use

You can use the agent directly:
```python
from src.agent import ArticleGeneratorAgent
agent = ArticleGeneratorAgent()
specs = """Title: \"Intro to Rust for Python Developers\"\nAudience: Beginner\nNotes: Compare ownership with Python references."""
result = agent.generate_articles(specs)
for art in result.articles:
	 print(art.title)
	 print(art.content[:300], "...")
```




## 🏁 Summary
This app streamlines creation of structured, developer-friendly programming articles from simple textual specs using Google Gemini and Streamlit. Enter specs, generate, then browse rich Markdown results on the Blogs page.

