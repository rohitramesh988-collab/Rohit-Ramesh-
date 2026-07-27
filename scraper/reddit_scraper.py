"""Search Reddit for posts matching a query using Reddit's public search JSON endpoint.

No API key is required for this endpoint, but Reddit rate-limits aggressively without
a descriptive User-Agent, so always set one (see USER_AGENT below).
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterator

import requests

USER_AGENT = "reddit-quora-scraper/1.0 (by /u/research-tool)"
SEARCH_URL = "https://www.reddit.com/search.json"
SUBREDDIT_SEARCH_URL = "https://www.reddit.com/r/{subreddit}/search.json"


@dataclass
class RedditPost:
    title: str
    url: str
    permalink: str
    subreddit: str
    author: str
    score: int
    num_comments: int
    created_utc: float
    selftext: str

    def to_dict(self) -> dict:
        return self.__dict__


def search_reddit(
    query: str,
    limit: int = 25,
    subreddit: str | None = None,
    sort: str = "relevance",
    time_filter: str = "all",
    pause: float = 1.0,
) -> Iterator[RedditPost]:
    """Yield RedditPost results for `query`, paginating until `limit` is reached.

    `pause` seconds are slept between paginated requests to stay well under Reddit's
    rate limits.
    """
    url = SUBREDDIT_SEARCH_URL.format(subreddit=subreddit) if subreddit else SEARCH_URL
    headers = {"User-Agent": USER_AGENT}
    params = {"q": query, "sort": sort, "t": time_filter, "limit": min(limit, 100)}

    fetched = 0
    after = None
    while fetched < limit:
        if after:
            params["after"] = after
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        payload = resp.json()

        children = payload.get("data", {}).get("children", [])
        if not children:
            break

        for child in children:
            if fetched >= limit:
                break
            d = child.get("data", {})
            yield RedditPost(
                title=d.get("title", ""),
                url=d.get("url", ""),
                permalink="https://www.reddit.com" + d.get("permalink", ""),
                subreddit=d.get("subreddit", ""),
                author=d.get("author", ""),
                score=d.get("score", 0),
                num_comments=d.get("num_comments", 0),
                created_utc=d.get("created_utc", 0.0),
                selftext=d.get("selftext", ""),
            )
            fetched += 1

        after = payload.get("data", {}).get("after")
        if not after:
            break
        time.sleep(pause)
