import streamlit as st
import pandas as pd
from src.scrapper import LinkedInScapper


def get_scrapper() -> LinkedInScapper:
    """Return (and cache) a single scrapper instance for the app session."""
    if "scrapper" not in st.session_state:
        st.session_state.scrapper = LinkedInScapper()
    return st.session_state.scrapper


st.set_page_config(page_title="LinkedIn Profile Scraper", layout="wide")
st.title("🔍 LinkedIn Profile Scraper")
st.markdown(
    "Enter LinkedIn profile URLs separated by commas. We'll attempt to log in (using env credentials) and scrape public profile details into a table."
)

st.markdown("**Input format example:** `https://www.linkedin.com/in/john-doe/, https://www.linkedin.com/in/jane-smith/`")

raw_input = st.text_area(
    "LinkedIn profile URLs (comma separated)",
    placeholder="https://www.linkedin.com/in/john-doe/, https://www.linkedin.com/in/jane-smith/"
)

error_msg = None
parsed_links = []


def validate_and_parse(raw: str):
    links = []
    for part in [p.strip() for p in raw.split(",") if p.strip()]:
        # Basic validation: must start with LinkedIn profile prefix
        if not part.startswith("https://www.linkedin.com/in/"):
            raise ValueError(f"Invalid LinkedIn profile URL: {part}")
        links.append(part)
    if not links:
        raise ValueError("No valid profile links provided.")
    return links


col1, col2 = st.columns([1, 3])
with col1:
    scrape_btn = st.button("🚀 Scrape Profiles", type="primary")

if scrape_btn:
    try:
        parsed_links = validate_and_parse(raw_input)
    except ValueError as ve:
        error_msg = str(ve)

    if error_msg:
        st.error(error_msg)
    else:
        with st.spinner("Scraping profiles..."):
            try:
                scrapper = get_scrapper()
                result = scrapper.scrape(parsed_links)
                if isinstance(result, pd.DataFrame):
                    st.success("✅ Successfully scraped profiles!")
                    st.dataframe(result, use_container_width=True)
                else:
                    st.error(
                        "❌ An unexpected response was returned instead of a DataFrame.")
                    st.write(result)
            except Exception as e:
                st.error("❌ Some error occurred during scraping.")
                st.exception(e)
