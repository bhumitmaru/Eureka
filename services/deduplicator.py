from .data_cleaner import normalize_title

def deduplicate(papers):
    """Map ADT: DOI/title keys make duplicate lookup O(1)."""
    paper_map, kept = {}, []
    for paper in papers:
        key = ('doi:' + paper['doi']) if paper.get('doi') else ('title:' + normalize_title(paper['title']))
        if key not in paper_map:
            paper_map[key] = paper; kept.append(paper)
        else:
            existing = paper_map[key]
            if paper.get('citation_count', 0) > existing.get('citation_count', 0):
                existing.update(paper)
    return kept, len(papers) - len(kept)
