# from web_scraper import WebScraper
from text_cleaner import TextCleaner
import spacy
import csv
import os

# # Create an instance of the WebScraper class
# scraper = WebScraper()
# # Fetch the URLs from the sitemap
# urls = scraper.get_urls_in_sitemap("https://www.newyorklife.com/sitemap.xml")
# # Scrape each URL and save the contents to a text file
# scraper.save_to_files(urls)

# Initialize spaCy
nlp = spacy.load("en_core_web_lg")
# Initialize the TextCleaner with your list of common sentences
common_sentences = [
    "Understand what people like you typically consider when making their plans",
    "Being prepared looks different across all phases of life",
    "Account How-To Videos",
    "Contact Us We're here to listen: 1 (800) CALL-NYL Monday – Friday",
    "Receive resources & tools that can help you prepare for the future",
    "You can cancel anytime",
]
cleaner = TextCleaner(common_sentences, nlp)

# Open the CSV file and read the file names
with open("data/url_to_file_map.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    url_to_file_map = {rows[0]: rows[1] for rows in reader}

    # Iterate over the file names and clean each file
    for filename in url_to_file_map.values():
        # Open the file in read mode
        with open("data/" + filename, "r", encoding="utf-8") as f:
            text = f.read()
            # Clean the text in the file
            cleaned_text = cleaner.remove_common_sentences(text)

        # Write the cleaned text into a new file in the cleaned_web_scraped_data directory
        with open(
            "data/cleaned_web_scraped_data/" + filename, "w", encoding="utf-8"
        ) as f:
            f.write(cleaned_text)
