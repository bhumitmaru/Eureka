from .base import APIClient
from config import Config

class SemanticScholarAPI(APIClient):
    def search(self, query, page=1, limit=10):
        headers={'x-api-key':Config.SEMANTIC_SCHOLAR_API_KEY} if Config.SEMANTIC_SCHOLAR_API_KEY else {}
        d=self.get_json('https://api.semanticscholar.org/graph/v1/paper/search',{'query':query,'limit':limit,'offset':(page-1)*limit,'fields':'title,authors,year,abstract,citationCount,venue,openAccessPdf,externalIds,url'},headers) or {}
        return [{'title':p.get('title'),'authors':', '.join(a['name'] for a in p.get('authors',[])),'publication_year':p.get('year'),'journal':p.get('venue',''),'doi':(p.get('externalIds') or {}).get('DOI',''),'url':p.get('url',''),'citation_count':p.get('citationCount',0),'abstract':p.get('abstract',''),'source':'Semantic Scholar','open_access':bool(p.get('openAccessPdf'))} for p in d.get('data',[])]
