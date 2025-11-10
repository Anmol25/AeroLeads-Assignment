from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")


class Article(BaseModel):
    title: str = Field(..., description="Title of the article")
    content: str = Field(..., description="Content of the article")


class ArticlesOutput(BaseModel):
    article_generated: bool = Field(
        ..., description="Indicates if articles were generated, For eg. if user query does not contain any article specifications, this will be false")
    articles: Optional[List[Article]] = Field(None,
                                              description="List of generated articles")


SYSTEM_PROMPT = """
You are a helpful assistant specialized in writing high-quality programming articles.

Behavior and output format requirements:

1) For each article specification the user provides (a title and optional details/requirements), generate exactly one complete article in well-formed GitHub-Flavored Markdown. If the user supplies multiple specifications, produce one article per specification and separate articles with a horizontal rule (---).

2) Each article MUST begin with a Markdown heading and inline meta:
    - First line: an H2 heading with the Title (e.g., `## My Article Title`).
    - Second line: Summary as 1–2 sentences.

Example:

## My Article Title
One-line summary.

3) After the title/summary/meta lines, include a concise Table of Contents (with links to headings), then the article body using clear headings (##, ###).

4) For programming articles include:
    - Short, runnable code examples inside fenced code blocks with the correct language identifier.
    - Explanations for code snippets and step-by-step reasoning.
    - Example input/output where relevant and small sample datasets or command examples.
    - Notes on common pitfalls, performance considerations, and alternatives.

5) Keep the tone educational and practical. Target audience: software developers and engineers. When the user specifies audience level, follow it; otherwise default to Intermediate.

6) Default length when unspecified: aim for ~500–600 words per article. If user asks for shorter or longer, obey that constraint.

7) Do not include non-markdown wrappers (no extra JSON or commentary outside the Markdown) unless the user explicitly requests a machine-readable format. Output MUST be valid Markdown only.

8) If the user provides implementation constraints (frameworks, languages, example inputs, or style), follow them exactly. If details are missing, ask a clarifying question only when necessary; otherwise assume reasonable defaults stated above.

9) When asked to produce multiple articles in one response, ensure each article follows the same structure and is clearly separated.

Produce helpful, concise, and well-structured programming articles that a developer can read and use immediately.

Important: If the user query does not contain any article specifications, raise an error indicating that at least one specification is required.
"""


class ArticleGeneratorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_articles(self, prompt):
        """Generates programming articles based on user specifications."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "response_mime_type": "application/json",
                "response_json_schema": ArticlesOutput.model_json_schema(),
            },
        )
        articles = {}
        if response.text:
            articles = ArticlesOutput.model_validate_json(response.text)
        return articles


if __name__ == "__main__":
    agent = ArticleGeneratorAgent()
    user_query = """
Please generate five programming articles (one article per specification). Follow your Markdown rules. Specifications:

1) Title: "Introduction to Rust for Python Developers"
   Audience: Beginner
   Language: Rust
   Notes: Compare with Python, cover ownership/borrowing, include simple runnable examples.

2) Title: "Building REST APIs with FastAPI"
   Audience: Intermediate
   Language: Python
   Notes: Include a minimal FastAPI app, Dockerfile, deployment tips, and common pitfalls."""

    articles = agent.generate_articles(user_query)
    if articles:
        print(articles.model_dump_json(indent=2))
        with open("generated_articles.json", "w") as f:
            f.write(articles.model_dump_json(indent=2))
