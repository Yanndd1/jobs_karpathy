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
        with open("scores.json", encoding="utf-8") as f:
            scores_list = json.load(f)
        scores = {s["slug"]: s for s in scores_list}

    # Load observed exposure (Anthropic Economic Index, mars 2026), indicateur
    # complémentaire, produit par build_observed_exposure.py
    observed = {}
    observed_path = "external_data/anthropic_observed_exposure_fr.json"
    if os.path.exists(observed_path):
        with open(observed_path, encoding="utf-8") as f:
            observed = {k: v for k, v in json.load(f).items() if v}

    # Rattachement aux familles professionnelles Dares, produit par refresh_stats_fr.py
    dares = {}
    dares_path = "external_data/dares_stats_fr.json"
    if os.path.exists(dares_path):
        with open(dares_path, encoding="utf-8") as f:
            dares = {d["slug"]: d for d in json.load(f)}

    # Load CSV stats
    csv_file = "metiers.csv" if os.path.exists("metiers.csv") else "occupations.csv"
    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Detect French vs US format
    is_french = "salaire_median_annuel" in rows[0] if rows else False

    # Merge
    data = []
    for row in rows:
        slug = row["slug"]
        score = scores.get(slug, {})
        obs = observed.get(slug)
        dar = dares.get(slug)

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
                "observed": obs["observed_exposure"] if obs else None,
                "observed_soc": obs["soc_title"] if obs else None,
                "fap": " + ".join(dar["fap_labels"]) if dar else None,
                "fap_partage": dar["n_partage"] if dar and dar["n_partage"] > 1 else None,
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
    with open("site/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    print(f"Wrote {len(data)} métiers to site/data.json")
    total_jobs = sum(d["jobs"] for d in data if d["jobs"])
    print(f"Total emplois représentés : {total_jobs:,}")


if __name__ == "__main__":
    main()
