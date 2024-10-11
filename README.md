# Ai-project-utills
A small set of utillities that i use in regards to my AI data project about looking at reviews and finding new patterns in large data.

scrape-trust.py :

This script uses Selenium and BeautifulSoup to scrape customer reviews from Trustpilot. It collects review details such as title, body, rating, and date for each review and saves them to individual CSV files for each page. The script also implements checkpointing to resume scraping from where it left off.
Libraries and Dependencies

    time: Used to handle delays between page loads.
    random: Generates random delays to simulate human behavior and avoid detection.
    os: Manages file operations for checkpointing.
    pandas: Handles data storage in CSV format.
    BeautifulSoup: Parses the HTML content to extract review data.
    selenium: Automates web interactions.
    webdriver_manager: Automatically manages the Selenium WebDriver installation.

Main Components

    extract_reviews():
    Extracts review details (title, body, rating, date) from the current page's HTML source using BeautifulSoup.

    apply_random_delay(page_number):
    Implements random delays between page requests to mimic human behavior and avoid triggering rate limits.

    scrape_multiple_pages(start_page, end_page, resume):
    Loops through multiple pages, extracts reviews, saves them to CSV, and handles checkpointing for resumed scraping.

    Checkpoints:
    The script saves a record of completed pages to "scraped_pages.txt" to enable resumption if interrupted.

Usage

    Set up the base URL with the desired company ID for Trustpilot.
    Configure start and end pages for scraping.
    Run the script and monitor progress through printed statements and saved CSV files.

Important Considerations

    Dynamic Content Loading:
    The script uses Selenium's WebDriverWait to handle dynamic content.
    Anti-Bot Measures:
    Randomized delays and periodic longer breaks are applied to reduce detection risk.

createjsonfromcsv:
Overview

This script converts Trustpilot review CSV files into structured JSON format. It processes each CSV file in the specified directory, converts its content into JSON objects, and saves the resulting data in a separate JSON file for each CSV file.