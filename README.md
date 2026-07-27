# Reddit & Quora Post Scraper

A small CLI tool for searching Reddit and Quora for posts/questions matching a topic.

## Install

```bash
pip install -r requirements.txt

# Optional, only needed for the more reliable Quora backend:
pip install playwright
playwright install chromium
```

## Usage

```bash
# Search both sites
python -m scraper.cli "prompt engineering"

# Reddit only, restrict to a subreddit, limit results
python -m scraper.cli "prompt engineering" --source reddit --subreddit MachineLearning --limit 10

# Quora only, using the headless-browser backend (more reliable than plain requests)
python -m scraper.cli "prompt engineering" --source quora --quora-engine playwright

# Write results to a file instead of stdout
python -m scraper.cli "prompt engineering" --output results.json
python -m scraper.cli "prompt engineering" --output results.csv
```

## How it works

- **Reddit**: uses Reddit's public `search.json` endpoint. No API key required, but a
  descriptive `User-Agent` is sent to avoid being rate-limited. See
  `scraper/reddit_scraper.py`.
- **Quora**: Quora has no public search API and is heavily JS-rendered, so two
  backends are provided (`scraper/quora_scraper.py`):
  - `requests` (default): fast, dependency-light, parses Quora's embedded
    `__NEXT_DATA__` JSON. Quora sometimes serves a login wall to anonymous HTTP
    clients, in which case this backend returns no results.
  - `playwright`: renders the search page in a real headless browser, which is
    much more reliable against Quora's client-side rendering and login gating.
    Requires the optional `playwright` dependency above.

## Notes

- Both sites' HTML/JSON structure can change at any time, which may break parsing —
  the code is written defensively (returns an empty list rather than crashing) but
  may need small updates if a site changes its markup.
- Respect each site's Terms of Service and rate limits; this tool adds a short pause
  between paginated Reddit requests and does not attempt to bypass Quora's
  authentication.
