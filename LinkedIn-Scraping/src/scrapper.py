import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from typing import List
from dotenv import load_dotenv
import os

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

    def scrape_experience(self, link):
        """Scrape Experience by navigating to experience page."""
        self.driver.get(link + "details/experience/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        return "Processing Experience section..."

    def scrape_education(self, link):
        """Scrape Education by navigating to education page."""
        self.driver.get(link + "details/education/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        return "Processing Education section..."

    def scrape_certifications(self, link):
        """Scrape Certifications by navigating to certifications page."""
        self.driver.get(link + "details/certifications/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        return "Processing Licenses & certifications section..."

    def scrape_projects(self, link):
        """Scrape Projects by navigating to projects page."""
        self.driver.get(link + "details/projects/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        return "Processing Projects section..."

    def scrape_skills(self, link):
        """Scrape Skills by navigating to skills page."""
        self.driver.get(link + "details/skills/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        skills = card.find_elements(
            By.CSS_SELECTOR, "div.display-flex.align-items-center.mr1.hoverable-link-text.t-bold span[aria-hidden='true']")
        skill_list = [skill.text for skill in skills if skill.text.strip()]

        return skill_list

    def scrape_publications(self, link):
        """Scrape Publications by navigating to publications page."""
        self.driver.get(link + "details/publications/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        return "Processing Publications section..."

    def scrape_courses(self, link):
        """Scrape Courses by navigating to courses page."""
        self.driver.get(link + "details/courses/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        return "Processing Courses section..."

    def scrape_awards(self, link):
        """Scrape Honors & awards by navigating to honors & awards page."""
        self.driver.get(link + "details/honors/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        return "Processing Honors & awards section..."

    def scrape_languages(self, link):
        """Scrape Languages by navigating to languages page."""
        self.driver.get(link + "details/languages/")
        time.sleep(3)
        card = self.driver.find_element(
            By.CSS_SELECTOR, "section.artdeco-card.pb3")
        return "Processing Languages section..."

    def scrape_sections(self, columns, link):
        """Scrape only those columns which are awailable in profile and allowed."""
        switch = {
            "Experience": self.scrape_experience,
            "Education": self.scrape_education,
            "Licenses & certifications": self.scrape_certifications,
            "Projects": self.scrape_projects,
            "Skills": self.scrape_skills,
            "Publications": self.scrape_publications,
            "Courses": self.scrape_courses,
            "Honors & awards": self.scrape_awards,
            "Languages": self.scrape_languages
        }
        results = {}

        for column in columns:
            if column in self.allowed_columns and column in switch:
                results[column] = switch[column](link)

        return results

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
        education = cards[0].find_elements(
            By.CSS_SELECTOR, "ul li span.t-black")[1].text
        # Scrape About Section
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
            "Education": education,
            "Location": location,
            "About": about_body
        }

        return profile_data

    def scrape_profile(self, link):
        """Scrape a single LinkedIn profile."""
        self.driver.get(link)
        time.sleep(1)
        columns = []
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, "h2.pvs-header__title span[aria-hidden='true']")
        for i, element in enumerate(elements):
            print(f"Element no. {i}")
            text = self.driver.execute_script(
                "return arguments[0].textContent;", element).strip()
            columns.append(text)
        print("columns found on the profile:")
        for column in columns:
            print(column)
        time.sleep(1)
        cards = self.driver.find_elements(By.CLASS_NAME, "artdeco-card")
        profile_data = self.scrape_user_info(cards[:2])
        sections_data = self.scrape_sections(
            columns=columns, link=self.driver.current_url)
        final_dict = profile_data | sections_data
        return final_dict

    def scrape(self, links: List[str]):
        """Main function to scrape multiple LinkedIn profiles."""
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(1)
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
        return results
