"""
Build a CSV summary of all French occupations from scraped data.

Reads from html/<slug>.json (API data) or html/<slug>.html and metiers.json.
Integrates employment and salary data from INSEE/DARES where available.
Writes to metiers.csv.

Usage:
    uv run python make_csv_fr.py
    uv run python make_csv_fr.py --with-stats emploi_stats.json
"""

import csv
import json
import os
import re
import argparse


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def extract_from_api_json(json_path, meta):
    """Extract structured data from a France Travail API JSON response."""
    with open(json_path) as f:
        data = json.load(f)

    row = {
        "title": meta["title"],
        "category": meta["category"],
        "slug": meta["slug"],
        "code_rome": meta.get("code_rome", data.get("code", "")),
        "salaire_median_annuel": "",
        "salaire_median_mensuel": "",
        "niveau_formation": "",
        "experience_requise": "",
        "nb_emplois": "",
        "nb_emplois_projete": "",
        "perspectives_pct": "",
        "perspectives_desc": "",
        "variation_emploi": "",
        "url": meta.get("url", ""),
    }

    # Extract education level from access conditions
    acces = data.get("acces", data.get("conditionAcces", ""))
    if acces:
        acces_lower = acces.lower()
        if "doctorat" in acces_lower or "bac+8" in acces_lower:
            row["niveau_formation"] = "Doctorat (Bac+8)"
        elif "master" in acces_lower or "bac+5" in acces_lower:
            row["niveau_formation"] = "Master (Bac+5)"
        elif "licence" in acces_lower or "bac+3" in acces_lower:
            row["niveau_formation"] = "Licence (Bac+3)"
        elif "bts" in acces_lower or "dut" in acces_lower or "bac+2" in acces_lower:
            row["niveau_formation"] = "BTS/DUT (Bac+2)"
        elif "bac pro" in acces_lower or "bac professionnel" in acces_lower:
            row["niveau_formation"] = "Bac professionnel"
        elif "baccalauréat" in acces_lower or "bac " in acces_lower:
            row["niveau_formation"] = "Baccalauréat"
        elif "cap" in acces_lower or "bep" in acces_lower:
            row["niveau_formation"] = "CAP/BEP"
        elif "aucun diplôme" in acces_lower or "sans diplôme" in acces_lower:
            row["niveau_formation"] = "Sans diplôme"

    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-stats", type=str, default=None,
        help="Path to a JSON file with employment/salary stats per ROME code"
    )
    args = parser.parse_args()

    with open("metiers.json") as f:
        metiers = json.load(f)

    # Load optional external stats (from INSEE/DARES)
    ext_stats = {}
    if args.with_stats and os.path.exists(args.with_stats):
        with open(args.with_stats) as f:
            stats_data = json.load(f)
        for entry in stats_data:
            key = entry.get("code_rome", entry.get("slug", ""))
            if key:
                ext_stats[key] = entry

    fieldnames = [
        "title", "category", "slug", "code_rome",
        "salaire_median_annuel", "salaire_median_mensuel",
        "niveau_formation", "experience_requise",
        "nb_emplois", "nb_emplois_projete",
        "perspectives_pct", "perspectives_desc", "variation_emploi",
        "url",
    ]

    rows = []
    missing = 0

    for m in metiers:
        slug = m["slug"]
        json_path = f"html/{slug}.json"
        html_path = f"html/{slug}.html"

        if os.path.exists(json_path):
            row = extract_from_api_json(json_path, m)
        elif os.path.exists(html_path):
            # Basic row from metadata only
            row = {field: "" for field in fieldnames}
            row["title"] = m["title"]
            row["category"] = m["category"]
            row["slug"] = m["slug"]
            row["code_rome"] = m.get("code_rome", "")
            row["url"] = m.get("url", "")
        else:
            # No scraped data, create from metadata
            row = {field: "" for field in fieldnames}
            row["title"] = m["title"]
            row["category"] = m["category"]
            row["slug"] = m["slug"]
            row["code_rome"] = m.get("code_rome", "")
            row["url"] = m.get("url", "")
            missing += 1

        # Merge external stats if available
        code = m.get("code_rome", "")
        if code in ext_stats:
            stats = ext_stats[code]
            for key in ["salaire_median_annuel", "salaire_median_mensuel",
                        "nb_emplois", "nb_emplois_projete", "perspectives_pct",
                        "perspectives_desc", "variation_emploi"]:
                if key in stats and stats[key]:
                    row[key] = stats[key]
        elif slug in ext_stats:
            stats = ext_stats[slug]
            for key in ["salaire_median_annuel", "salaire_median_mensuel",
                        "nb_emplois", "nb_emplois_projete", "perspectives_pct",
                        "perspectives_desc", "variation_emploi"]:
                if key in stats and stats[key]:
                    row[key] = stats[key]

        # Impute monthly from annual if missing
        if row["salaire_median_annuel"] and not row["salaire_median_mensuel"]:
            try:
                row["salaire_median_mensuel"] = str(
                    round(float(row["salaire_median_annuel"]) / 12)
                )
            except ValueError:
                pass
        elif row["salaire_median_mensuel"] and not row["salaire_median_annuel"]:
            try:
                row["salaire_median_annuel"] = str(
                    round(float(row["salaire_median_mensuel"]) * 12)
                )
            except ValueError:
                pass

        rows.append(row)

    with open("metiers.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to metiers.csv (missing source: {missing})")

    # Sample
    print(f"\nExemples :")
    for r in rows[:3]:
        sal = r['salaire_median_annuel'] or '?'
        emp = r['nb_emplois'] or '?'
        print(f"  {r['title']}: {sal}€/an, {emp} emplois")


if __name__ == "__main__":
    main()
