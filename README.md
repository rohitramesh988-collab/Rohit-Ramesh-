# Job Search Tracker

State repo for a Claude Code routine that pulls live LinkedIn job matches every weekday at 10:00 AM.

## Target profile

- **Titles:** SEO, AEO, GEO, AI SEO — Assistant Manager or Manager level
- **Location:** Bengaluru
- **Experience:** 7+ years
- **Background:** technical SEO, on-page optimization, content and internal linking strategy, AEO/GEO strategy execution, WordPress/CMS management, paid media (Google Ads, Meta Ads), organic social growth
- **Source:** LinkedIn only, via the Bright Data connector

## How it works

1. The routine runs on the weekday 10:00 AM schedule.
2. It searches and scrapes live LinkedIn job postings matching the profile above.
3. It checks `seen-postings.md` and skips any URL already listed there.
4. New matches are written to `jobs-YYYY-MM-DD.md` (today's date) and committed.
5. New URLs are appended to `seen-postings.md` and committed.

## Files

- `seen-postings.md` — running list of LinkedIn job URLs already surfaced, used for dedup
- `jobs-YYYY-MM-DD.md` — one file per run day, only created when there are new matches

## Maintenance

`seen-postings.md` grows over time. Periodically trim entries for roles that are long closed if the file gets unwieldy — this has no effect on routine correctness, just tidiness.
