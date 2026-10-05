from .base import APIClient
from config import Config

class CrossrefAPI(APIClient):
    def search(self, query, page=1, rows=15):
        params={'query':query,'rows':rows,'offset':(page-1)*rows}
        if Config.CROSSREF_EMAIL: params['mailto']=Config.CROSSREF_EMAIL
        data=self.get_json('https://api.crossref.org/works',params) or {}
        out=[]
        for w in data.get('message',{}).get('items',[]):
            auth=', '.join(' '.join(filter(None,[a.get('given'),a.get('family')])) for a in w.get('author',[]))
            dates=w.get('published-print') or w.get('published-online') or {}; parts=dates.get('date-parts',[[]])[0]
            out.append({'title':(w.get('title') or [''])[0],'authors':auth,'publication_year':parts[0] if parts else None,
             'journal':(w.get('container-title') or [''])[0],'doi':w.get('DOI',''),'url':w.get('URL',''),
             'citation_count':w.get('is-referenced-by-count',0),'abstract':w.get('abstract',''),'source':'Crossref','open_access':False})
        return out
