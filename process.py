"""
Process scraped data files into Markdown.

Reads from html/<slug>.json or html/<slug>.html, writes to pages/<slug>.md.
Uses parse_rome.parse_metier() for French ROME data.

Usage:
    uv run python process.py              # process all files
    uv run python process.py --force      # re-process even if .md exists
"""

import argparse
import json
import os
from parse_rome import parse_metier


def main():
    parser = argparse.ArgumentParser(description="Convert scraped data to Markdown")
    parser.add_argument("--force", action="store_true", help="Re-process even if .md exists")
    args = parser.parse_args()

    os.makedirs("pages", exist_ok=True)

    # Load master list
    with open("metiers.json") as f:
        metiers = json.load(f)

    processed = 0
    skipped = 0
    missing = 0

    for m in metiers:
        slug = m["slug"]
        # Try JSON first (API data), then HTML (web data)
        json_path = f"html/{slug}.json"
        html_path = f"html/{slug}.html"
        md_path = f"pages/{slug}.md"

        if os.path.exists(json_path):
            source_path = json_path
        elif os.path.exists(html_path):
            source_path = html_path
        else:
            missing += 1
            continue

        if not args.force and os.path.exists(md_path):
            skipped += 1
            continue

        try:
            md = parse_metier(source_path)
            with open(md_path, "w") as f:
                f.write(md)
            processed += 1
        except Exception as e:
            print(f"Error processing {slug}: {e}")

    total_sources = len([f for f in os.listdir("html")
                         if f.endswith(".json") or f.endswith(".html")])
    total_md = len([f for f in os.listdir("pages") if f.endswith(".md")]) if os.path.exists("pages") else 0
    print(f"Processed: {processed}, Skipped (cached): {skipped}, Missing source: {missing}")
    print(f"Total: {total_sources} source files, {total_md} Markdown files")


if __name__ == "__main__":
    main()
