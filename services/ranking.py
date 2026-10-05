from .data_cleaner import normalize_title
from datetime import datetime

def score(paper, query):
    terms = set(normalize_title(query).split()); title = set(normalize_title(paper['title']).split())
    abstract = set(normalize_title(paper.get('abstract', '')).split())
    match = len(terms & title) * 22 + len(terms & abstract) * 5
    recency = max(0, (paper.get('publication_year') or 0) - (datetime.now().year - 8)) * 2
    citations = min(18, int(paper.get('citation_count', 0) / 20))
    return min(100, match + recency + citations)

def rank(papers, query):
    for p in papers: p['relevance'] = score(p, query)
    return sorted(papers, key=lambda x: x['relevance'], reverse=True)
