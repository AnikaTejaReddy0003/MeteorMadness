#!/usr/bin/env python3
"""
Fetch all Near-Earth Objects from NASA NeoWs /browse and save to neowsdata.json

- Follows links["next"] until exhausted (2000+ pages).
- Retries on 429 / 5xx with exponential backoff.
- Streams output to a single JSON array without loading all data in memory.
"""

import os
import sys
import time
import json
import math
import requests
from urllib.parse import urlparse, parse_qs

API_KEY = os.getenv("NASA_API_KEY", "NkXlYjwvpiIY0f2ReQBEkoIgvvVd24Fdeo65Jp71")
START_URL = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={API_KEY}"
OUTPUT_FILE = "neowsdata.json"

# ---- Tuning ----
MAX_RETRIES = 6
INITIAL_BACKOFF = 1.0  # seconds
RATE_DELAY = 0.2       # polite delay between successful requests

def fetch_with_retries(url: str, session: requests.Session) -> dict:
    """GET with retry/backoff on 429/5xx."""
    backoff = INITIAL_BACKOFF
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=60)
            if resp.status_code == 200:
                return resp.json()
            # Handle rate-limit or transient
            if resp.status_code in (429, 500, 502, 503, 504):
                # Try Retry-After if provided
                retry_after = resp.headers.get("Retry-After")
                sleep_for = float(retry_after) if retry_after else backoff
                print(f"[warn] HTTP {resp.status_code}; retrying in {sleep_for:.1f}s (attempt {attempt}/{MAX_RETRIES})")
                time.sleep(sleep_for)
                backoff = min(backoff * 2, 60)  # cap backoff
                continue
            # Hard error
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[warn] Request error: {e}; retrying in {backoff:.1f}s (attempt {attempt}/{MAX_RETRIES})")
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
    raise RuntimeError(f"Failed to fetch after {MAX_RETRIES} attempts: {url}")

def main():
    session = requests.Session()
    url = START_URL

    total_written = 0
    page_count = 0

    print(f"[info] Starting from: {url}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("[\n")  # begin JSON array
        first_item = True

        while url:
            data = fetch_with_retries(url, session)

            # Progress info if available
            page = data.get("page", {})
            number = page.get("number")
            total_pages = page.get("total_pages")
            size = page.get("size")

            neos = data.get("near_earth_objects", []) or []
            page_count += 1

            # Write NEOs one-by-one to avoid huge memory usage
            for neo in neos:
                if not first_item:
                    f.write(",\n")
                json.dump(neo, f, ensure_ascii=False)
                first_item = False
                total_written += 1

            print(f"[info] Page {number}/{total_pages - 1 if total_pages else '?'} "
                  f"size={size} | cumulative NEOs={total_written}")

            # Follow pagination
            links = data.get("links", {})
            next_url = links.get("next")
            url = next_url if next_url else None

            # Be polite to the API
            time.sleep(RATE_DELAY)

        f.write("\n]\n")  # close JSON array

    print(f"[done] Saved {total_written} NEO records to {OUTPUT_FILE} across {page_count} page(s).")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[cancelled] Interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(2)
