import html, re
from urllib.parse import urlparse

def clean_text(value):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', str(value or '')))).strip()

def normalize_title(title):
    return re.sub(r'[^a-z0-9 ]', '', clean_text(title).lower()).strip()

def valid_url(url):
    try: return urlparse(url or '').scheme in {'http', 'https'}
    except ValueError: return False

def clean_paper(raw):
    title = clean_text(raw.get('title'))
    if not title: return None
    try: year = int(raw.get('publication_year') or 0) or None
    except (ValueError, TypeError): year = None
    return {**raw, 'title': title, 'authors': clean_text(raw.get('authors')),
            'abstract': clean_text(raw.get('abstract')), 'journal': clean_text(raw.get('journal')),
            'doi': clean_text(raw.get('doi')).lower(), 'publication_year': year,
            'citation_count': int(raw.get('citation_count') or 0),
            'url': raw.get('url') if valid_url(raw.get('url')) else '',
            'open_access': bool(raw.get('open_access'))}
