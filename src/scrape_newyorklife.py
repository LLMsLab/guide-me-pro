from web_scraper import WebScraper


if __name__ == "__main__":
    scraper = WebScraper()

    # Fetch the URLs from the sitemap
    urls = scraper.get_urls_in_sitemap(
        "https://www.newyorklife.com/sitemap.xml"
    )

    # Scrape each URL and save the contents to a text file
    scraper.save_to_files(urls)
