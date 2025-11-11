import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from typing import List
from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd

load_dotenv()


class LinkedInScapper:
    def __init__(self):
        self.chromedriver_path = "./chromedriver-linux64/chromedriver"
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("user-data-dir=selenium_profile")
        options.add_argument("--profile-directory=Default")
        # Initialize driver
        service = Service(self.chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.linkedin_id = os.getenv("LINKEDIN_ID")
        self.linkedin_pass = os.getenv("LINKEDIN_PASS")
        self.allowed_columns = ["Experience", "Education", "Licenses & certifications", "Projects",
                                "Skills", "Publications", "Courses", "Honors & awards", "Languages"]

    def login(self):
        """Login to LinkedIn using provided credentials."""
        try:
            email_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
        except NoSuchElementException:
            try:
                details_btn = self.driver.find_element(
                    By.CSS_SELECTOR, "button.member-profile__details")
                try:
                    details_btn.click()
                    # Fill Captcha
                    time.sleep(30)
                except ElementClickInterceptedException:
                    # If click is intercepted, try via JS as a last resort
                    self.driver.execute_script(
                        "arguments[0].click();", details_btn)
                # small wait for UI to update
                time.sleep(1)
                # retry locating the login fields once
                email_field = self.driver.find_element(By.ID, "username")
                password_field = self.driver.find_element(By.ID, "password")
            except Exception:
                # fallback failed, cannot locate login fields
                return False

        # Enter Value
        email_field.send_keys(self.linkedin_id)
        password_field.send_keys(self.linkedin_pass)
        # Locate and click "Sign in" button
        time.sleep(1)
        sign_in_button = self.driver.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Sign in"]')
        sign_in_button.click()
        # Fill captcha
        time.sleep(30)
        # Check if login was successful
        if "LinkedIn" in self.driver.title:
            return True
        else:
            return False

    def scrape_user_info(self, cards):
        """Scrape User Info and about section from the profile."""
        # Scrape User Info
        name = cards[0].find_element(By.CSS_SELECTOR, "h1").text
        headline = cards[0].find_element(
            By.CSS_SELECTOR, "div.text-body-medium").text
        location = cards[0].find_element(
            By.CSS_SELECTOR, "span.text-body-small.inline.t-black--light.break-words").text
        company = cards[0].find_elements(
            By.CSS_SELECTOR, "ul li span.t-black")[0].text
        about_elem = cards[1].find_element(
            By.CSS_SELECTOR, "h2.pvs-header__title span[aria-hidden='true']")
        about_text = about_elem.text.strip()
        about_body = ""
        if about_text.lower() == "about":
            # Step 2: Extract the 'About' section text
            about_elem = cards[1].find_element(
                By.CSS_SELECTOR, "div.inline-show-more-text--is-collapsed span[aria-hidden='true']")
            about_body = about_elem.text.strip()

        # Format Data
        profile_data = {
            "Name": name,
            "Headline": headline,
            "Company": company,

            "Location": location,
            "About": about_body
        }

        return profile_data

    def scrape_sections(self, cards):
        """Scrape various sections from the profile safely, avoiding missing element errors."""
        final_dict = {}

        for card in cards:
            # Scrape heading
            try:
                heading_el = card.find_element(
                    By.CSS_SELECTOR, "h2.pvs-header__title span[aria-hidden='true']")
                heading = heading_el.text.strip()
                if heading not in self.allowed_columns:
                    continue  # skip unwanted sections
            except NoSuchElementException:
                heading = "Unknown Section"
                continue  # fallback name if heading missing
            # Scrape items under the heading
            try:
                items = card.find_elements(By.TAG_NAME, "li")
            except NoSuchElementException:
                items = []

            item_list = []
            for id, item in enumerate(items):
                try:
                    text = item.text.strip()
                    if text:  # optional: skip empty ones
                        item_list.append({"id": id, "item": text})
                except Exception as e:
                    print(f"Skipping item due to error: {e}")
                    continue

            final_dict[heading] = item_list

        return final_dict

    def scrape_profile(self, link):
        """Scrape a single LinkedIn profile."""
        self.driver.get(link)
        time.sleep(3)
        cards = self.driver.find_elements(By.CLASS_NAME, "artdeco-card")
        profile_data = self.scrape_user_info(cards[:2])
        sections_data = self.scrape_sections(
            cards=cards[2:])  # pass remaining cards for sections
        final_dict = profile_data | sections_data
        return final_dict

    def results_to_dataframe_and_csv(self, results, csv_path: str = "scraped_profiles/linkedin_data.csv") -> pd.DataFrame:
        """Convert scraped results to a pandas DataFrame and persist to CSV."""
        # Normalize input to a list of records
        records = results if isinstance(results, list) else [results]

        # Convert nested structures to JSON strings for stable CSV columns
        normalized_records = []
        for rec in records:
            safe_rec = {}
            for k, v in rec.items():
                if isinstance(v, (dict, list)):
                    try:
                        safe_rec[k] = json.dumps(v, ensure_ascii=False)
                    except Exception:
                        safe_rec[k] = str(v)
                else:
                    safe_rec[k] = v
            normalized_records.append(safe_rec)

        df = pd.DataFrame(normalized_records)

        # Ensure target directory exists
        csv_file = Path(csv_path)
        csv_file.parent.mkdir(parents=True, exist_ok=True)

        # Write or append accordingly with column alignment when appending
        if csv_file.exists():
            try:
                existing_cols = pd.read_csv(csv_file, nrows=0).columns.tolist()
                # Ensure all existing columns are present; drop extras to keep consistency
                for col in existing_cols:
                    if col not in df.columns:
                        df[col] = None
                df = df.reindex(columns=existing_cols)
            except Exception:
                # If header cannot be read, fall back to appending as-is without header
                pass
            df.to_csv(csv_file, mode="a", index=False, header=False)
        else:
            df.to_csv(csv_file, index=False)

        return df

    def scrape(self, links: List[str]):
        """Main function to scrape multiple LinkedIn profiles."""
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(3)
        print(self.driver.title)
        # Check if already logged in
        if self.driver.title == "LinkedIn Login, Sign in | LinkedIn":
            response = self.login()
            if not response:
                return {"status": "error", "error": "Cannot LogIn Successfully"}
        # time.sleep(50)
        results = []
        for link in links:
            results.append(self.scrape_profile(link))

        df = self.results_to_dataframe_and_csv(results)
        self.driver.quit()
        return df
