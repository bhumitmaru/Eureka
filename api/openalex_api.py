from .base import APIClient

class OpenAlexAPI(APIClient):
    def search(self, query, page=1, per_page=15):
        data = self.get_json('https://api.openalex.org/works', {'search':query,'page':page,'per-page':per_page}) or {}
        results=[]
        for w in data.get('results', []):
            authors=', '.join(a.get('author',{}).get('display_name','') for a in w.get('authorships',[]))
            inv=w.get('abstract_inverted_index') or {}; abstract=' '.join(inv.keys())
            loc=w.get('primary_location') or {}; source=(loc.get('source') or {}).get('display_name','')
            results.append({'title':w.get('title'),'authors':authors,'publication_year':w.get('publication_year'),
             'journal':source,'doi':w.get('doi','').replace('https://doi.org/',''),'url':w.get('doi') or w.get('id'),
             'citation_count':w.get('cited_by_count',0),'abstract':abstract,'source':'OpenAlex',
             'open_access':(w.get('open_access') or {}).get('is_oa',False)})
        return results
