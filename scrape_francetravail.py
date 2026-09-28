"""
Scrape France Travail API (ROME) to fetch occupation descriptions.

Uses the France Travail API (api.francetravail.io) with OAuth2 authentication
to download ROME occupation data. Saves raw JSON to html/<slug>.json as source
of truth, and optionally scrapes the Métierscope web pages for richer data.

Usage:
    uv run python scrape_francetravail.py                          # scrape all
    uv run python scrape_francetravail.py --start 0 --end 5        # first 5
    uv run python scrape_francetravail.py --force                  # re-scrape
    uv run python scrape_francetravail.py --mode web               # scrape web pages
    uv run python scrape_francetravail.py --mode api               # use API only

Caching: skips any occupation where html/<slug>.json already exists.

Requires in .env:
    FRANCE_TRAVAIL_CLIENT_ID=your_client_id
    FRANCE_TRAVAIL_CLIENT_SECRET=your_client_secret
"""

import argparse
import json
import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# France Travail API OAuth2
# ---------------------------------------------------------------------------
TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
API_BASE = "https://api.francetravail.io/partenaire/rome/v2"

_token_cache = {"token": None, "expires": 0}


def get_access_token(client):
    """Get OAuth2 access token from France Travail API."""
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires"] - 30:
        return _token_cache["token"]

    client_id = os.environ.get("FRANCE_TRAVAIL_CLIENT_ID", "")
    client_secret = os.environ.get("FRANCE_TRAVAIL_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        raise ValueError(
            "FRANCE_TRAVAIL_CLIENT_ID and FRANCE_TRAVAIL_CLIENT_SECRET "
            "must be set in .env"
        )

    resp = client.post(
        f"{TOKEN_URL}?realm=/partenaire",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "api_rome-metiersv2 nomenclatureRome",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    resp.raise_for_status()
    data = resp.json()
    _token_cache["token"] = data["access_token"]
    _token_cache["expires"] = now + data.get("expires_in", 1500)
    return _token_cache["token"]


# ---------------------------------------------------------------------------
# API scraping
# ---------------------------------------------------------------------------
def fetch_metier_api(client, code_rome):
    """Fetch a single ROME occupation from the API."""
    token = get_access_token(client)
    resp = client.get(
        f"{API_BASE}/metier/{code_rome}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_all_metiers_api(client):
    """Fetch the full list of ROME occupations from the API."""
    token = get_access_token(client)
    resp = client.get(
        f"{API_BASE}/metier",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Web scraping (Métierscope pages)
# ---------------------------------------------------------------------------
def scrape_metierscope(slug, url):
    """Scrape a Métierscope page using Playwright for richer HTML content."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
            if resp and resp.status == 200:
                html = page.content()
                return html
        except Exception as e:
            print(f"Web scrape error for {slug}: {e}")
        finally:
            browser.close()
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Scrape France Travail ROME data")
    parser.add_argument("--start", type=int, default=0, help="Start index")
    parser.add_argument("--end", type=int, default=None, help="End index")
    parser.add_argument("--force", action="store_true", help="Re-scrape")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between requests")
    parser.add_argument(
        "--mode", choices=["api", "web", "both"], default="api",
        help="Scraping mode: api (France Travail API), web (Métierscope pages), both"
    )
    parser.add_argument(
        "--discover", action="store_true",
        help="Discover all ROME occupations from API and save to metiers_api.json"
    )
    args = parser.parse_args()

    os.makedirs("html", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("pages", exist_ok=True)

    client = httpx.Client()

    # Discovery mode: fetch all occupations from API
    if args.discover:
        print("Discovering all ROME occupations from API...")
        try:
            all_metiers = fetch_all_metiers_api(client)
            with open("metiers_api.json", "w") as f:
                json.dump(all_metiers, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(all_metiers)} occupations to metiers_api.json")
        except Exception as e:
            print(f"Discovery failed: {e}")
            print("Using local metiers.json instead.")
        client.close()
        return

    # Load occupation list
    with open("metiers.json") as f:
        metiers = json.load(f)

    end = args.end if args.end is not None else len(metiers)
    subset = metiers[args.start:end]

    # Check cache
    to_scrape = []
    for i, m in enumerate(subset, start=args.start):
        json_path = f"html/{m['slug']}.json"
        html_path = f"html/{m['slug']}.html"
        cached = os.path.exists(json_path) or os.path.exists(html_path)
        if not args.force and cached:
            print(f"  [{i}] CACHED {m['title']}")
            continue
        to_scrape.append((i, m))

    if not to_scrape:
        print("Nothing to scrape - all cached.")
        client.close()
        return

    print(f"\nScraping {len(to_scrape)} occupations (mode: {args.mode})...\n")

    for idx, (i, m) in enumerate(to_scrape):
        slug = m["slug"]
        code_rome = m.get("code_rome", "")
        print(f"  [{i}] {m['title']} ({code_rome})...", end=" ", flush=True)

        # API scraping
        if args.mode in ("api", "both") and code_rome:
            try:
                api_data = fetch_metier_api(client, code_rome)
                json_path = f"html/{slug}.json"
                with open(json_path, "w") as f:
                    json.dump(api_data, f, indent=2, ensure_ascii=False)
                print(f"API OK", end=" ")
            except Exception as e:
                print(f"API ERROR: {e}", end=" ")

        # Web scraping
        if args.mode in ("web", "both"):
            url = m.get("url", "")
            if url:
                html = scrape_metierscope(slug, url)
                if html:
                    html_path = f"html/{slug}.html"
                    with open(html_path, "w") as f:
                        f.write(html)
                    print(f"WEB OK ({len(html):,} bytes)", end=" ")
                else:
                    print("WEB FAIL", end=" ")

        print()

        if idx < len(to_scrape) - 1:
            time.sleep(args.delay)

    client.close()

    cached_json = len([f for f in os.listdir("html") if f.endswith(".json")])
    cached_html = len([f for f in os.listdir("html") if f.endswith(".html")])
    print(f"\nDone. {cached_json} JSON + {cached_html} HTML files in html/")


if __name__ == "__main__":
    main()
