# Eureka — Academic Documentation

## Problem statement
Students often search papers and conference opportunities across disconnected sites. Eureka combines selected public REST APIs and carefully bounded, permission-aware scraping into one searchable platform.

## Objectives and scope
The system retrieves paper metadata, cleans and deduplicates it, ranks it with explainable rules, stores searches in SQLite, exports CSV, and presents trends. Conference collection is intentionally limited to permitted public sources and a page limit. It does not bypass CAPTCHAs or claim exhaustive coverage.

## Methodology and data flow
`Search → OpenAlex/Crossref/Semantic Scholar + permitted conference pages → validation → hash-map deduplication → ranking → SQLite → dashboard/CSV`.

## Functional requirements
Topic search, source selection, saved result browsing, paper details, conference view, dashboard, CSV export, live/demo mode. Non-functional requirements include responsive UI, bounded retries/timeouts, request delay, graceful source failure, and no hard-coded secret.

## Database design
`papers` stores normalized metadata and score; `conferences` stores public event details; `searches` records queries and counts. SQLite makes deployment suitable for a mini project.

## Results, limitations, and future scope
Demo mode provides three realistic records and two conference leads. Live results depend on source availability and metadata quality. Future work: source-specific CFP parsers after permission review, user accounts, saved alerts, and richer related-paper graphs.

## Conclusion
Eureka demonstrates a practical, ethical pipeline for research discovery while exposing the web-scraping and REST API concepts required by the course.
