from .base import APIClient

class EuropePMCAPI(APIClient):
    """Europe PMC public REST search, particularly useful for health research."""
    def search(self, query, page=1, page_size=15):
        data=self.get_json('https://www.ebi.ac.uk/europepmc/webservices/rest/search',{
            'query':query, 'format':'json', 'pageSize':page_size, 'page':page,
            'resultType':'core', 'sort':'CITED desc'}) or {}
        results=[]
        for p in data.get('resultList',{}).get('result',[]):
            doi=p.get('doi','')
            url=(p.get('fullTextUrlList') or {}).get('fullTextUrl', [{}])[0].get('url','')
            url=url or (f'https://europepmc.org/article/{p.get("source", "MED")}/{p.get("id", "")}' if p.get('id') else '')
            results.append({'title':p.get('title',''),'authors':p.get('authorString',''),
                'publication_year':p.get('pubYear'), 'journal':p.get('journalTitle',''), 'doi':doi,
                'url':url, 'citation_count':p.get('citedByCount',0), 'abstract':p.get('abstractText',''),
                'source':'Europe PMC', 'open_access':p.get('isOpenAccess') == 'Y'})
        return results
