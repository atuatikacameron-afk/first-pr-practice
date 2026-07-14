# First PR Practice

This is a small practice repo for learning the GitHub pull request workflow.

## About

This repo was created to practice the full flow of making a change,
opening a pull request, and merging it on GitHub.

## Goals

- Create a repository
- Make a small, safe improvement
- Open a pull request
- Review and merge it

Feel free to use this repo to keep practicing the workflow whenever you'd like.

## Truform Meta Ad Library Monitor

Checks Meta's public [Ad Library](https://www.facebook.com/ads/library/) for
ads run by Truform and reports any new ads or ads that stopped running since
the last check.

### Setup

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in:
   - `META_ACCESS_TOKEN` — an access token from a Meta app that has been
     granted **Ad Library API access**. Regular Graph API permissions
     (`ads_read`, etc.) are not enough — the app itself must go through
     Meta's Ad Library API access process at
     https://www.facebook.com/ads/library/api, which includes identity
     confirmation.
   - `TRUFORM_SEARCH_TERM` — defaults to `Truform`.
   - `AD_REACHED_COUNTRIES` — comma-separated country codes to search
     (defaults to `US`).
3. `python3 main.py`

### How it works

- `meta_ads_monitor/ad_library.py` queries the `ads_archive` endpoint for all
  ads matching the search term, paginating through results.
- `meta_ads_monitor/state.py` compares the current results against the
  previous run (saved in `data/ad_library_state.json`, gitignored) to find
  new ads and ads that just stopped running.
- `meta_ads_monitor/report.py` formats a plain-text summary.
- `main.py` ties it together and updates the saved state after each run.

This only covers publicly listed Ad Library entries. It does not access
Truform's private Ads Manager account (spend, performance metrics) — that
would require a separate token with `ads_read` permission on the ad account.
