"""
Generate prompt.md — a single file containing all project data, designed to be
copy-pasted into an LLM for analysis and conversation about AI exposure of the
French job market.

Usage:
    uv run python make_prompt.py
"""

import csv
import json
import os


def fmt_pay(pay):
    if pay is None:
        return "?"
    return f"{pay:,} €".replace(",", " ")


def fmt_jobs(jobs):
    if jobs is None:
        return "?"
    if jobs >= 1_000_000:
        return f"{jobs / 1e6:.1f}M"
    if jobs >= 1_000:
        return f"{jobs / 1e3:.0f}K"
    return str(jobs)


def main():
    # Load all data sources
    with open("metiers.json") as f:
        metiers = json.load(f)

    csv_file = "metiers.csv" if os.path.exists("metiers.csv") else "occupations.csv"
    is_french = os.path.exists("metiers.csv")

    with open(csv_file) as f:
        csv_rows = {row["slug"]: row for row in csv.DictReader(f)}

    scores = {}
    if os.path.exists("scores.json"):
        with open("scores.json") as f:
            scores = {s["slug"]: s for s in json.load(f)}

    # Merge into unified records
    records = []
    for m in metiers:
        slug = m["slug"]
        row = csv_rows.get(slug, {})
        score = scores.get(slug, {})

        if is_french:
            pay = int(row["salaire_median_annuel"]) if row.get("salaire_median_annuel") else None
            jobs = int(row["nb_emplois"]) if row.get("nb_emplois") else None
            outlook_pct = int(row["perspectives_pct"]) if row.get("perspectives_pct") else None
            outlook_desc = row.get("perspectives_desc", "")
            education = row.get("niveau_formation", "")
        else:
            pay = int(row["median_pay_annual"]) if row.get("median_pay_annual") else None
            jobs = int(row["num_jobs_2024"]) if row.get("num_jobs_2024") else None
            outlook_pct = int(row["outlook_pct"]) if row.get("outlook_pct") else None
            outlook_desc = row.get("outlook_desc", "")
            education = row.get("entry_education", "")

        records.append({
            "title": m["title"],
            "slug": slug,
            "category": row.get("category", m.get("category", "")),
            "code_rome": m.get("code_rome", ""),
            "pay": pay,
            "jobs": jobs,
            "outlook_pct": outlook_pct,
            "outlook_desc": outlook_desc,
            "education": education,
            "exposure": score.get("exposure"),
            "rationale": score.get("rationale", ""),
            "url": m.get("url", ""),
        })

    # Sort by exposure desc, then jobs desc
    records.sort(key=lambda r: (-(r["exposure"] or 0), -(r["jobs"] or 0)))

    nb_metiers = len(records)
    lines = []

    # -- Header --
    lines.append("# Exposition à l'IA du marché du travail français")
    lines.append("")
    lines.append(
        f"Ce document contient des données structurées sur {nb_metiers} métiers "
        "français issus du répertoire ROME (Répertoire Opérationnel des Métiers "
        "et des Emplois) de France Travail, chacun évalué sur une échelle "
        "d'exposition à l'IA de 0 à 10 par un LLM. Utilisez ces données pour "
        "analyser, questionner et discuter de l'impact de l'IA sur le marché "
        "du travail français."
    )
    lines.append("")
    lines.append("Sources de données : France Travail (ROME), INSEE, DARES")
    lines.append("")

    # -- Scoring methodology --
    lines.append("## Méthodologie de scoring")
    lines.append("")
    lines.append(
        "Chaque métier a été évalué sur un axe unique d'Exposition à l'IA "
        "de 0 à 10, mesurant dans quelle mesure l'IA va transformer ce métier. "
        "Le score prend en compte à la fois l'automatisation directe (l'IA "
        "réalisant le travail) et les effets indirects (l'IA rendant les "
        "travailleurs si productifs que moins de personnes sont nécessaires)."
    )
    lines.append("")
    lines.append(
        "Un heuristique clé : si le métier peut être exercé entièrement depuis "
        "un bureau à domicile sur un ordinateur — écrire, coder, analyser, "
        "communiquer — alors l'exposition à l'IA est intrinsèquement élevée (7+). "
        "Les spécificités françaises (cadre réglementaire, AI Act européen, "
        "droit du travail, métiers réglementés) sont prises en compte."
    )
    lines.append("")
    lines.append("Repères de calibration :")
    lines.append("- 0-1 Minimale : couvreurs, maçons, jardiniers-paysagistes")
    lines.append("- 2-3 Faible : électriciens, plombiers, sapeurs-pompiers, aides-soignants")
    lines.append("- 4-5 Modérée : infirmiers, policiers, vétérinaires, éducateurs spécialisés")
    lines.append("- 6-7 Élevée : enseignants, comptables, journalistes, conseillers bancaires")
    lines.append("- 8-9 Très élevée : développeurs, designers graphiques, traducteurs, data analysts")
    lines.append("- 10 Maximale : opérateurs de saisie, télévendeurs")
    lines.append("")

    # -- Aggregate statistics --
    lines.append("## Statistiques agrégées")
    lines.append("")

    total_jobs = sum(r["jobs"] or 0 for r in records)
    total_wages = sum((r["jobs"] or 0) * (r["pay"] or 0) for r in records)

    # Weighted avg exposure
    w_sum = sum(
        (r["exposure"] or 0) * (r["jobs"] or 0)
        for r in records if r["exposure"] is not None and r["jobs"]
    )
    w_count = sum(
        r["jobs"] or 0 for r in records if r["exposure"] is not None and r["jobs"]
    )
    w_avg = w_sum / w_count if w_count else 0

    lines.append(f"- Nombre de métiers : {len(records)}")
    lines.append(f"- Total emplois : {total_jobs:,}".replace(",", " "))
    if total_wages > 0:
        lines.append(f"- Masse salariale annuelle : {total_wages/1e9:.1f} Md€")
    lines.append(f"- Exposition IA moyenne (pondérée par l'emploi) : {w_avg:.1f}/10")
    lines.append("")

    # Tier breakdown
    tiers = [
        ("Minimale (0-1)", 0, 1),
        ("Faible (2-3)", 2, 3),
        ("Modérée (4-5)", 4, 5),
        ("Élevée (6-7)", 6, 7),
        ("Très élevée (8-10)", 8, 10),
    ]
    lines.append("### Répartition par niveau d'exposition")
    lines.append("")
    lines.append("| Niveau | Métiers | Emplois | % emplois |")
    lines.append("|--------|---------|---------|-----------|")
    for name, lo, hi in tiers:
        group = [r for r in records if r["exposure"] is not None and lo <= r["exposure"] <= hi]
        jobs = sum(r["jobs"] or 0 for r in group)
        pct = jobs / total_jobs * 100 if total_jobs else 0
        lines.append(f"| {name} | {len(group)} | {fmt_jobs(jobs)} | {pct:.1f}% |")
    lines.append("")

    # By education
    lines.append("### Exposition moyenne par niveau de formation (pondérée)")
    lines.append("")
    edu_groups = [
        ("Sans diplôme / CAP-BEP", ["Sans diplôme", "CAP/BEP"]),
        ("Bac", ["Baccalauréat", "Bac professionnel"]),
        ("Bac+2", ["BTS/DUT (Bac+2)"]),
        ("Bac+3 (Licence)", ["Licence (Bac+3)"]),
        ("Bac+5 (Master)", ["Master (Bac+5)"]),
        ("Bac+8 (Doctorat)", ["Doctorat (Bac+8)"]),
    ]
    lines.append("| Formation | Exposition moy. | Emplois |")
    lines.append("|-----------|----------------|---------|")
    for name, matches in edu_groups:
        group = [
            r for r in records
            if r["education"] in matches and r["exposure"] is not None and r["jobs"]
        ]
        if group:
            ws = sum(r["exposure"] * r["jobs"] for r in group)
            wc = sum(r["jobs"] for r in group)
            lines.append(f"| {name} | {ws/wc:.1f} | {fmt_jobs(wc)} |")
    lines.append("")

    # -- Full occupation table --
    lines.append(f"## Les {nb_metiers} métiers")
    lines.append("")
    lines.append("Triés par exposition à l'IA (décroissant), puis par nombre d'emplois.")
    lines.append("")

    for score_val in range(10, -1, -1):
        group = [r for r in records if r["exposure"] == score_val]
        if not group:
            continue
        group_jobs = sum(r["jobs"] or 0 for r in group)
        lines.append(
            f"### Exposition {score_val}/10 ({len(group)} métiers, "
            f"{fmt_jobs(group_jobs)} emplois)"
        )
        lines.append("")
        lines.append("| # | Métier | Salaire | Emplois | Formation | Explication |")
        lines.append("|---|--------|---------|---------|-----------|-------------|")
        for i, r in enumerate(group, 1):
            edu = r["education"] if r["education"] else "?"
            rationale = r["rationale"].replace("|", "/").replace("\n", " ") if r["rationale"] else ""
            lines.append(
                f"| {i} | {r['title']} | {fmt_pay(r['pay'])} | "
                f"{fmt_jobs(r['jobs'])} | {edu} | {rationale} |"
            )
        lines.append("")

    # Write
    text = "\n".join(lines)
    with open("prompt.md", "w") as f:
        f.write(text)

    print(f"Wrote prompt.md ({len(text):,} chars, {len(lines):,} lines)")


if __name__ == "__main__":
    main()
