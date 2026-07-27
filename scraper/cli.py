"""CLI: search Reddit and Quora for posts matching a query.

Examples:
    python -m scraper.cli "prompt engineering"
    python -m scraper.cli "prompt engineering" --source reddit --limit 10
    python -m scraper.cli "prompt engineering" --source quora --quora-engine playwright
    python -m scraper.cli "prompt engineering" --output out.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys

from scraper.reddit_scraper import search_reddit
from scraper.quora_scraper import search_quora


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search Reddit and Quora for posts.")
    parser.add_argument("query", help="Search term/topic to look for")
    parser.add_argument(
        "--source",
        choices=["reddit", "quora", "all"],
        default="all",
        help="Which site(s) to search (default: all)",
    )
    parser.add_argument("--limit", type=int, default=25, help="Max results per source")
    parser.add_argument("--subreddit", default=None, help="Restrict Reddit search to one subreddit")
    parser.add_argument(
        "--quora-engine",
        choices=["requests", "playwright"],
        default="requests",
        help="Backend for Quora search (default: requests; use playwright for reliability)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Write results to this file (.json or .csv). Defaults to stdout as JSON.",
    )
    return parser.parse_args(argv)


def collect_results(args: argparse.Namespace) -> list[dict]:
    results: list[dict] = []

    if args.source in ("reddit", "all"):
        for post in search_reddit(args.query, limit=args.limit, subreddit=args.subreddit):
            row = post.to_dict()
            row["source"] = "reddit"
            results.append(row)

    if args.source in ("quora", "all"):
        for result in search_quora(args.query, limit=args.limit, engine=args.quora_engine):
            row = result.to_dict()
            row["source"] = "quora"
            results.append(row)

    return results


def write_results(results: list[dict], output: str | None) -> None:
    if not output:
        json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return

    if output.endswith(".csv"):
        if not results:
            open(output, "w").close()
            return
        fieldnames = sorted({key for row in results for key in row})
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    else:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        results = collect_results(args)
    except Exception as exc:  # surface a clean error instead of a traceback
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    write_results(results, args.output)
    if args.output:
        print(f"Wrote {len(results)} result(s) to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
