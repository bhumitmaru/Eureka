import logging, time, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import Config

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=.6, status_forcelist=[429,500,502,503,504], allowed_methods=['GET'])
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
    def get_json(self, url, params=None, headers=None):
        time.sleep(Config.REQUEST_DELAY)
        try:
            r = self.session.get(url, params=params, headers=headers, timeout=12)
            r.raise_for_status(); return r.json()
        except (requests.RequestException, ValueError) as exc:
            logging.warning('Request failed for %s: %s', url, exc); return None
