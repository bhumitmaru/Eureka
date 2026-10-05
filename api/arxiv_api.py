"""arXiv Atom API integration — no credentials required."""
import time
import xml.etree.ElementTree as ET
from .base import APIClient
from config import Config

class ArxivAPI(APIClient):
    def search(self, query, page=1, per_page=15):
        # arXiv requests callers leave a 3-second gap between successive calls.
        time.sleep(max(3, Config.REQUEST_DELAY))
        try:
            response = self.session.get('https://export.arxiv.org/api/query', params={
                'search_query': f'all:{query}', 'start': (page - 1) * per_page,
                'max_results': per_page, 'sortBy': 'relevance', 'sortOrder': 'descending'}, timeout=20)
            response.raise_for_status()
            root = ET.fromstring(response.content)
        except Exception:
            return []
        atom = '{http://www.w3.org/2005/Atom}'
        results=[]
        for entry in root.findall(f'{atom}entry'):
            links=entry.findall(f'{atom}link')
            pdf=next((x.get('href') for x in links if x.get('title') == 'pdf'), '')
            published=(entry.findtext(f'{atom}published') or '')[:4]
            results.append({'title':entry.findtext(f'{atom}title',''),
                'authors':', '.join(x.findtext(f'{atom}name','') for x in entry.findall(f'{atom}author')),
                'publication_year':published, 'journal':'arXiv preprint', 'doi':'',
                'url':pdf or entry.findtext(f'{atom}id',''), 'citation_count':0,
                'abstract':entry.findtext(f'{atom}summary',''), 'source':'arXiv', 'open_access':True})
        return results
