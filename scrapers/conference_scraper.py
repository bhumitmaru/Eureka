from .base_scraper import StaticScraper
from .dynamic_scraper import DynamicScraper

class ConferenceScraper:
    """Reusable, page-limited conference page collector; configure only permitted sources."""
    def collect_static(self, urls, max_pages=3):
        records=[]
        for url in urls[:max(0,min(max_pages,10))]:
            try:
                soup=StaticScraper().fetch(url)
                # CSS selector requirement: page heading; source-specific fields can extend this.
                name=(soup.select_one('h1, h2') or {}).get_text(' ',strip=True)
                if name: records.append({'name':name,'url':url,'source':'Static website'})
            except Exception: continue
        return records
    def collect_dynamic_demo(self, url):
        # XPath requirement, used only when a user chooses a JS-rendered permitted page.
        return DynamicScraper().extract_text_xpath(url, '//h1 | //h2')
