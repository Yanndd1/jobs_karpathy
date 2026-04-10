"""
Build a compact JSON for the website by merging CSV stats with AI exposure scores.

Reads metiers.csv (for stats) and scores.json (for AI exposure).
Writes site/data.json.

Usage:
    uv run python build_site_data.py
"""

import csv
import json
import os


def main():
    # Load AI exposure scores
    scores = {}
    if os.path.exists("scores.json"):
        with open("scores.json") as f:
            scores_list = json.load(f)
        scores = {s["slug"]: s for s in scores_list}

    # Load CSV stats
    csv_file = "metiers.csv" if os.path.exists("metiers.csv") else "occupations.csv"
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Detect French vs US format
    is_french = "salaire_median_annuel" in rows[0] if rows else False

    # Merge
    data = []
    for row in rows:
        slug = row["slug"]
        score = scores.get(slug, {})

        if is_french:
            data.append({
                "title": row["title"],
                "slug": slug,
                "category": row["category"],
                "code_rome": row.get("code_rome", ""),
                "pay": int(row["salaire_median_annuel"]) if row.get("salaire_median_annuel") else None,
                "jobs": int(row["nb_emplois"]) if row.get("nb_emplois") else None,
                "outlook": int(row["perspectives_pct"]) if row.get("perspectives_pct") else None,
                "outlook_desc": row.get("perspectives_desc", ""),
                "education": row.get("niveau_formation", ""),
                "exposure": score.get("exposure"),
                "exposure_rationale": score.get("rationale"),
                "url": row.get("url", ""),
            })
        else:
            data.append({
                "title": row["title"],
                "slug": slug,
                "category": row["category"],
                "pay": int(row["median_pay_annual"]) if row.get("median_pay_annual") else None,
                "jobs": int(row["num_jobs_2024"]) if row.get("num_jobs_2024") else None,
                "outlook": int(row["outlook_pct"]) if row.get("outlook_pct") else None,
                "outlook_desc": row.get("outlook_desc", ""),
                "education": row.get("entry_education", ""),
                "exposure": score.get("exposure"),
                "exposure_rationale": score.get("rationale"),
                "url": row.get("url", ""),
            })

    os.makedirs("site", exist_ok=True)
    with open("site/data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False)

    print(f"Wrote {len(data)} métiers to site/data.json")
    total_jobs = sum(d["jobs"] for d in data if d["jobs"])
    print(f"Total emplois représentés : {total_jobs:,}")


if __name__ == "__main__":
    main()
