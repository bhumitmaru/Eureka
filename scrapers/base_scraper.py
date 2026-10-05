import time, requests
from bs4 import BeautifulSoup
from config import Config

class StaticScraper:
    """Safe static scraper: requests + BeautifulSoup CSS selectors."""
    def fetch(self, url):
        time.sleep(Config.REQUEST_DELAY)
        r=requests.get(url, timeout=12, headers={'User-Agent':'Eureka academic project (polite research tool)'})
        r.raise_for_status(); return BeautifulSoup(r.text,'lxml')
    def extract_links(self, url, selector='a'):
        return [(a.get_text(' ',strip=True),a.get('href')) for a in self.fetch(url).select(selector)]
