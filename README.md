# Eureka

**Discover Research. Discover Opportunities.** Eureka is a Flask-based academic discovery app that helps users search for research papers and relevant conference opportunities from multiple sources, clean and rank the results, and view them in a simple dashboard.

## Project overview

This project is designed to behave like a lightweight research assistant for a student or researcher. A user types a topic such as "deep learning in health informatics" or "graph neural networks". The app then:

- queries multiple public academic sources in parallel,
- cleans and normalizes metadata,
- removes duplicates,
- ranks the results based on relevance to the query,
- stores search history in SQLite,
- presents the results on paper listing and detail pages,
- shows an overview dashboard and CSV export for saved items.

In short, Eureka turns messy metadata from several academic APIs into a more usable, searchable, and explainable result set.

## How the app works

1. The user enters a topic on the homepage or search page.
2. The Flask app calls `search_papers()` in `app.py`.
3. Depending on `DEMO_MODE`, it either reads from `data/sample_data.csv` or calls public APIs such as OpenAlex, Crossref, Semantic Scholar, arXiv, and Europe PMC.
4. Each API result is cleaned by `services/data_cleaner.py` to validate fields like URLs and years and normalize titles.
5. Duplicate papers are removed with `services/deduplicator.py`.
6. Results are scored using `services/ranking.py`, which calculates a relevance score based on the original query and paper metadata.
7. The cleaned, ranked papers are saved into the SQLite database via `database/db.py`.
8. The user can browse saved papers, inspect a single paper, check a conference list, review analytics, or export CSV data.

## Main features
- Live public paper search through OpenAlex, Crossref, Semantic Scholar, arXiv, and Europe PMC
- Reliable **Demo Mode** backed by local CSV for viva/offline demonstration
- Cleaning, URL/year validation, normalised-title/DOI deduplication, and explainable relevance score
- SQLite history, paper detail pages, conference view, dashboard charts, responsive UI, and CSV export
- Reusable static BeautifulSoup/CSS-selector and Selenium/XPath scraper classes
- Request timeout, retry/backoff on 429/5xx, configurable polite delay, and graceful source failure

## Install and run

```bash
cd "/Users/bhumit/Desktop/Sem 5/project"
python -m venv venv
source venv/bin/activate              # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                  # Windows: copy .env.example .env
python app.py
```

Open `http://127.0.0.1:5000`. Database tables initialise automatically at first start. `DEMO_MODE=true` is the recommended presentation setting. Set it to `false` for live APIs. Optional credentials belong only in `.env`; never commit it. Selenium uses Selenium Manager with a locally installed Chrome/Chromium browser.

## Project structure

- `app.py` — routes, orchestration, export
- `api/` — isolated REST clients with query parameters and pagination
- `scrapers/` — static Requests/BeautifulSoup and dynamic Selenium examples
- `services/` — cleaning, Map ADT deduplication, ranking
- `database/db.py` — SQLite schema and persistence
- `templates/`, `static/` — Flask UI and Chart.js analytics
- `data/sample_data.csv` — demo data; `tests/` — essential unit tests

## Testing

```bash
python -m unittest discover -s tests -v
```

## Data sources and API behaviour
OpenAlex, Crossref, arXiv, and Europe PMC require no key for ordinary public use. Semantic Scholar can use `SEMANTIC_SCHOLAR_API_KEY` when provided. `page`, `per_page`/`rows`, and offsets demonstrate pagination. arXiv responses are Atom XML and use a minimum three-second spacing in line with its API guidance; other API calls use timeouts, retries with exponential backoff, status handling, and JSON validation. Do not send high-volume requests.

## Scraping methodology and ethics
`StaticScraper` makes polite Requests requests and parses CSS selectors; `DynamicScraper` uses Selenium and XPath only for JS-rendered pages. `ConferenceScraper` hard-limits pages (maximum ten) and is a generic extension point rather than a crawler. Check robots.txt and site terms, use official APIs when available, do not bypass access controls/CAPTCHAs, and collect only public, non-sensitive data.

## Mapping to Course Experiments

| Experiment | Demonstration |
|---|---|
| EXP1 | `scrapers/base_scraper.py`: Requests + BeautifulSoup + CSS selector |
| EXP2 | `scrapers/dynamic_scraper.py`: Selenium + XPath |
| EXP3 | `DynamicScraper.extract_text_xpath()` for JavaScript-rendered permitted pages |
| EXP4 | `ConferenceScraper.collect_static()` page limit and exception handling |
| EXP5 | `api/openalex_api.py`, `api/crossref_api.py` REST requests |
| EXP6 | pagination params, `.env` key/email configuration, retry handling |
| EXP7 | `services/data_cleaner.py`, `deduplicator.py`, and CSV export |

## API and schema
The API clients return a common paper dictionary: title, authors, year, journal, DOI, URL, citations, abstract, source, and OA status. SQLite includes `papers`, `conferences`, and `searches`; see `database/db.py` for the executable schema.

## Limitations and future scope
Search quality depends on upstream metadata. Current conference content is a safe demo dataset plus reusable collection architecture, not a claim to scrape every conference directory. Possible enhancements: approved source adapters, alerts, user libraries, and improved author/topic graphs.
