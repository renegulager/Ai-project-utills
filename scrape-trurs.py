import time
import random
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Base URL for Trustpilot JYSK DK reviews with all languages
base_url = "https://www.trustpilot.com/review/XXXX/languages=all&page={}&sort=recency"

# Set up Selenium WebDriver with Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Increase WebDriverWait timeout to allow time for dynamic content to load
wait = WebDriverWait(driver, 40)

# Function to extract reviews from the current page
def extract_reviews():
    """Extract reviews from the current page source."""
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews = soup.find_all("section", class_="styles_reviewContentwrapper__zH_9M")
    page_reviews = []

    for review in reviews:
        try:
            title = review.find("h2", class_="typography_heading-s__f7029").text.strip() if review.find("h2", class_="typography_heading-s__f7029") else None
            body = review.find("p", class_="typography_body-l__KUYFJ").text.strip() if review.find("p", class_="typography_body-l__KUYFJ") else None
            rating = review.find("img").get("alt") if review.find("img") else None
            date = review.find("time").get("datetime") if review.find("time") else None
            page_reviews.append({"rating": rating, "title": title, "body": body, "date": date})
        except Exception as e:
            print(f"Error extracting review: {e}")
    return page_reviews

# Function to implement adaptive delays based on current page number
def apply_random_delay(page_number):
    """Apply randomized delays between pages to simulate human behavior."""
    # Short random delay between 5 and 10 seconds for most pages
    delay = random.uniform(5, 10)

    # Every 50 pages, take a longer break of 1-3 minutes
    if page_number % 50 == 0:
        delay = random.uniform(60, 180)  # Longer delay between 1 to 3 minutes

    print(f"Delaying for {delay:.2f} seconds before the next page...")
    time.sleep(delay)

# Function to scrape reviews from multiple pages with throttling and progress tracking
def scrape_multiple_pages(start_page=1, end_page=1438, resume=False):
    """Scrape reviews from multiple pages, saving progress to a file."""
    completed_pages = set()

    # Load existing scraped pages if resume is enabled
    if resume and os.path.exists("scraped_pages.txt"):
        with open("scraped_pages.txt", "r") as f:
            completed_pages = set(int(line.strip()) for line in f.readlines())
        print(f"Resuming scraping. {len(completed_pages)} pages already scraped.")

    for page_number in range(start_page, end_page + 1):
        if page_number in completed_pages:
            print(f"Page {page_number} already scraped. Skipping...")
            continue

        print(f"Scraping page {page_number}...")
        page_url = base_url.format(page_number)
        driver.get(page_url)

        # Apply a random delay before processing the page
        apply_random_delay(page_number)

        try:
            # Wait for the reviews container to be present
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.styles_reviewContentwrapper__zH_9M")))

            # Extract reviews from the current page
            page_reviews = extract_reviews()
            print(f"Extracted {len(page_reviews)} reviews from page {page_number}.")

            # Save current page reviews to a separate CSV file
            df = pd.DataFrame(page_reviews)
            df.to_csv(f"trustpilot_reviews_page_{page_number}.csv", index=False)
            print(f"Page {page_number} saved as 'trustpilot_reviews_page_{page_number}.csv'.")

            # Log the completed page to the checkpoint file
            with open("scraped_pages.txt", "a") as f:
                f.write(f"{page_number}\n")

        except Exception as e:
            print(f"Error on page {page_number}: {e}")
            # Wait for a longer period before retrying to avoid bans
            long_delay = random.uniform(60, 180)  # Random delay between 1 to 3 minutes
            print(f"Encountered an error; waiting for {long_delay:.2f} seconds before retrying...")
            time.sleep(long_delay)

    print("Finished scraping all pages.")

# Start scraping from page 1 to xxxx with checkpointing and resumption support
scrape_multiple_pages(resume=True)

# Close the Selenium WebDriver
driver.quit()
