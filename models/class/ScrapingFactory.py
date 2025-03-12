import requests  # For making HTTP requests (simulated scraping)
from bs4 import BeautifulSoup  # For parsing HTML (simulated scraping)
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.class.ScrapingFrancetravail import ScrapingFrancetravail

class ScrapingFactory:
    domain = [
        "francetravail.fr",
    ]

    def __init__(self):
        pass

    def urlCheckInDomain(self, url):
        """
        Check if the given URL belongs to one of the supported domains.
        
        :param url: The URL to check.
        :return: True if the URL belongs to a supported domain, False otherwise.
        """
        for domain in self.domain:
            if domain in url:
                return True
        return False

    def scrapOne(self, url):
        """
        Scrape data from a single URL.
        
        :param url: The URL to scrape.
        :return: Scraped data or None if the URL is not supported.
        """
        if not self.urlCheckInDomain(url):
            print(f"URL {url} is not supported.")
            return None

        if "francetravail.fr" in url:
            scraper = ScrapingFrancetravail()
        else:
            return None

        return scraper.scrape(url)

    def scrapMany(self, keyWord):
        """
        Scrape multiple job listings based on a keyword.
        
        :param keyWord: The keyword to search for.
        :return: A list of scraped job listings.
        """
        if not keyWord:
            print("Keyword is required.")
            return []

        # Use the France Travail scraper for this example
        scraper = ScrapingFrancetravail()
        return scraper.scrapMany(keyWord)