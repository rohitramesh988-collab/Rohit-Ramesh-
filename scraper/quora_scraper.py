"""Search Quora for questions/posts matching a query.

Quora has no public search API and aggressively gates content behind login walls and
client-side JavaScript rendering, so two backends are provided:

- "requests": fast, no extra dependencies beyond `requests`, but Quora often serves a
  login wall or incomplete data to plain HTTP clients. Works best for a quick check.
- "playwright": renders the page in a real (headless) browser, which is far more
  reliable against Quora's JS-heavy search UI. Requires `pip install playwright`
  and `playwright install chromium` once.

Both backends return the same `QuoraResult` shape so callers don't need to care which
one produced the data.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Iterator

import requests

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
SEARCH_URL = "https://www.quora.com/search"


@dataclass
class QuoraResult:
    title: str
    url: str
    snippet: str

    def to_dict(self) -> dict:
        return self.__dict__


def _extract_next_data(html: str) -> dict | None:
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def _walk_for_questions(node, results: list[QuoraResult], seen: set[str]) -> None:
    """Recursively search Quora's embedded JSON state for question-like nodes."""
    if isinstance(node, dict):
        title = node.get("title") or node.get("question_title")
        url = node.get("url") or node.get("canonical_url")
        if title and url and url not in seen:
            seen.add(url)
            if not url.startswith("http"):
                url = "https://www.quora.com" + url
            results.append(QuoraResult(title=title, url=url, snippet=node.get("snippet", "")))
        for value in node.values():
            _walk_for_questions(value, results, seen)
    elif isinstance(node, list):
        for item in node:
            _walk_for_questions(item, results, seen)


def search_quora_requests(query: str, limit: int = 25) -> list[QuoraResult]:
    """Best-effort Quora search using a plain HTTP GET.

    Quora may return a login wall instead of search results for anonymous requests;
    in that case this returns an empty list. Prefer `search_quora_playwright` for
    reliable results.
    """
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    resp = requests.get(
        SEARCH_URL, headers=headers, params={"q": query, "type": "question"}, timeout=20
    )
    resp.raise_for_status()

    data = _extract_next_data(resp.text)
    results: list[QuoraResult] = []
    if data:
        _walk_for_questions(data, results, seen=set())
    return results[:limit]


def search_quora_playwright(query: str, limit: int = 25, headless: bool = True) -> list[QuoraResult]:
    """Quora search via a headless browser, for pages plain HTTP can't render."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "playwright is not installed. Run `pip install playwright` and "
            "`playwright install chromium` to use this backend."
        ) from exc

    results: list[QuoraResult] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(f"{SEARCH_URL}?q={query}&type=question", timeout=30000)
        page.wait_for_timeout(2500)  # let client-side rendering settle

        anchors = page.query_selector_all("a.q-box[href^='/']")
        seen: set[str] = set()
        for a in anchors:
            href = a.get_attribute("href") or ""
            text = (a.inner_text() or "").strip()
            if not text or href in seen:
                continue
            if not re.match(r"^/[^/]+\?", href) and "/" not in href[1:]:
                continue
            seen.add(href)
            results.append(
                QuoraResult(title=text, url="https://www.quora.com" + href, snippet="")
            )
            if len(results) >= limit:
                break

        browser.close()
    return results


def search_quora(
    query: str, limit: int = 25, engine: str = "requests"
) -> Iterator[QuoraResult]:
    """Dispatch to the chosen backend ("requests" or "playwright")."""
    if engine == "playwright":
        yield from search_quora_playwright(query, limit=limit)
    else:
        yield from search_quora_requests(query, limit=limit)
