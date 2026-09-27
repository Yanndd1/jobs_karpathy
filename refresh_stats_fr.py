"""
Rafraîchit les effectifs et les salaires des 147 métiers à partir des données DARES.

Sources (téléchargées dans external_data/, voir README) :
  - Dares, Portraits statistiques des métiers, édition du 16 juillet 2026
      * effectifs en emploi par famille professionnelle, 2004 à 2024 (enquête Emploi Insee)
      * salaire mensuel net médian par famille professionnelle, période 2023-2025
  - Dares, Table de passage Rome vers FAP-2021 (nomenclature FAP 2021)

Méthode
-------
Chaque métier du site est rattaché à une ou plusieurs familles professionnelles
(FAP 2021), la nomenclature métier de la Dares. La table de passage Rome -> FAP
sert de menu de candidats, mais le choix final est fait à la main dans FAP_MAP :
la correspondance Rome -> FAP est多 à plusieurs et comporte des rapprochements
inadaptés à notre découpage.

Deux cas particuliers, traités explicitement :

1. Métier couvrant plusieurs FAP. Beaucoup de métiers manuels sont scindés par la
   Dares en « peu qualifiés » et « qualifiés » (maçons, plombiers, soudeurs...).
   Notre métier couvre les deux : l'effectif est la somme, le salaire médian est la
   moyenne des médianes pondérée par les effectifs (approximation assumée, une
   moyenne de médianes n'est pas une médiane).

2. FAP partagée par plusieurs de nos métiers. La Dares ne distingue pas toujours
   ce que nous distinguons (avocats et juristes d'entreprise, télévendeurs et
   opérateurs de centre d'appels...). L'effectif de la FAP est alors réparti à
   parts égales entre les métiers concernés, pour que le total reste juste et que
   la surface du treemap ne compte pas deux fois les mêmes emplois. Le salaire
   n'est pas divisé. Le champ effectif_partage indique le nombre de métiers
   concernés.

Quand une FAP n'a pas de salaire publié à son niveau (secret statistique sur les
petits effectifs), on remonte la hiérarchie : FAP 341 -> FAP 228 -> FAP 86.

Usage :
    uv run python refresh_stats_fr.py            # écrit metiers.csv
    uv run python refresh_stats_fr.py --dry-run  # rapport seul, n'écrit rien
"""

import argparse
import csv
import json
import os
import sys
import xml.etree.ElementTree as ET
import zipfile

ED = "external_data"
EFF_XLSX = os.path.join(ED, "dares_psm_effectifs_2004_2024.xlsx")
SAL_XLSX = os.path.join(ED, "dares_psm_salaire_median.xlsx")
ANNEE_EFFECTIFS = 2024
PERIODE_SALAIRES = "2023-2025"

# Notre slug -> familles professionnelles FAP-2021 (Dares).
# Plusieurs codes = le métier couvre plusieurs FAP, les effectifs s'additionnent.
FAP_MAP = {
    # Gestion, administration
    "comptables": ["L1X60"],
    "controleurs-gestion": ["L4X81"],
    "experts-comptables": ["L5X90"],
    "auditeurs-financiers": ["L5X90"],
    "directeurs-financiers": ["L5X90"],
    "gestionnaires-paie": ["L4X80a"],
    "responsables-rh": ["L5X92"],
    "secretaires": ["L0X60a"],
    "assistants-direction": ["L3X80b"],
    "agents-accueil": ["L2X60"],
    "operateurs-saisie": ["L2X61"],
    "acheteurs": ["R4X90a"],
    "directeurs-generaux": ["L6X00"],
    # Informatique et télécoms
    "developpeurs-informatiques": ["M1X80", "M2X90"],
    "ingenieurs-informatique": ["M2X93"],
    "experts-cybersecurite": ["M2X93"],
    "administrateurs-systemes-reseaux": ["M1X81a", "M2X92a"],
    "chefs-projets-informatiques": ["M2X91"],
    "data-analysts": ["L5X93"],
    "techniciens-support-informatique": ["M1X81c"],
    "techniciens-telecoms": ["G1X75"],
    "webmasters": ["U1X82c"],
    # Santé
    "infirmiers-soins-generaux": ["V1X80a"],
    "aides-soignants": ["V0X60c"],
    "medecins-generalistes": ["V2X90"],
    "pharmaciens": ["V2X93a"],
    "kinesitherapeutes": ["V3X80c"],
    "chirurgiens-dentistes": ["V2X91"],
    "sages-femmes": ["V1X80d"],
    "psychologues": ["V3X90"],
    "opticiens-lunetiers": ["V3X71b"],
    "preparateurs-pharmacie": ["V3X70c"],
    "ambulanciers": ["J3X40a"],
    "manipulateurs-radiologie": ["V3X70b"],
    "techniciens-labo-medical": ["V3X70a"],
    "dieteticiens": ["V3X80a"],
    "orthophonistes": ["V3X80d"],
    "ergotherapeutes": ["V3X80b"],
    # Enseignement, formation, recherche
    "enseignants-secondaire": ["W0X90"],
    "enseignants-primaire": ["W0X80"],
    "formateurs": ["W1X80b"],
    "bibliothecaires": ["U0X91"],
    "chercheurs": ["N1X91"],
    # Droit et justice
    "avocats": ["L5X91"],
    "juristes-entreprise": ["L5X91"],
    "notaires": ["P3X90a"],
    "huissiers-justice": ["P3X90b"],
    "greffiers": ["P3X90b"],
    # Banque, assurance, immobilier
    "agents-immobiliers": ["R3X84", "R4X93a"],
    "conseillers-bancaires": ["QCX01"],
    "agents-assurance": ["QDX01", "QDX02"],
    "gestionnaires-patrimoine": ["QCX02"],
    "traders": ["QAX01"],
    "analystes-financiers": ["QAX02"],
    # Commerce et vente
    "vendeurs-magasin": ["R1X60", "R1X61", "R1X62"],
    "caissiers": ["R0X61"],
    "directeurs-magasin": ["R4X92"],
    "responsables-marketing": ["R4X90b"],
    "commerciaux-terrain": ["R2X80a", "R4X91"],
    "televendeurs": ["R1X67"],
    "operateurs-centre-appels": ["R1X67"],
    "chefs-produit": ["R3X83"],
    "boulangers-patissiers": ["S0X42"],
    "bouchers": ["S0X40"],
    # Communication et médias
    "designers-graphiques": ["U1X82c"],
    "journalistes": ["U0X92b"],
    "redacteurs-web": ["U0X80"],
    "community-managers": ["U0X80"],
    "charges-communication": ["U0X90"],
    "traducteurs-interpretes": ["U0X81"],
    "photographes": ["U1X81"],
    # Arts et spectacle
    "techniciens-audiovisuels": ["U1X80b"],
    "comediens": ["U1X91a"],
    "musiciens": ["U1X91a"],
    # Construction et BTP
    "macons": ["B1X30", "B1X31"],
    "electriciens-batiment": ["B2X32a", "B2X32b"],
    "plombiers-chauffagistes": ["B2X33a", "B2X33b"],
    "peintres-batiment": ["B2X36a", "B2X36b"],
    "charpentiers": ["B1X33a", "B1X33b"],
    "couvreurs": ["B1X34a", "B1X34b"],
    "carreleurs": ["B2X30a", "B2X30b"],
    "menuisiers": ["B2X37", "B2X38"],
    "conducteurs-travaux": ["B6X74"],
    "conducteurs-engins-chantier": ["B5X40b"],
    "architectes": ["B7X90"],
    "geometres-topographes": ["B6X70"],
    "ingenieurs-btp": ["B6X71a", "B7X91"],
    # Industrie
    "techniciens-maintenance-industrielle": ["G1X72a"],
    "soudeurs": ["D1X33a", "D1X33b"],
    "chaudronniers": ["D1X30a", "D1X30b"],
    "usineurs": ["D0X30", "D0X31"],
    "operateurs-production": ["E4X32a", "E4X32b"],
    "conducteurs-ligne-production": ["E2X20", "E2X40"],
    "techniciens-qualite": ["H0X90"],
    "ingenieurs-mecanique": ["N1X90"],
    "ingenieurs-energie": ["N1X90"],
    "ingenieurs-environnement": ["H1X91"],
    "mecaniciens-automobiles": ["G0B41b", "G0B41e"],
    "carrossiers": ["G0B40a", "G0B40b"],
    "mecaniciens-aeronautiques": ["G0A40c", "G1X72b"],
    "techniciens-electronique": ["G0A41", "G1X77b"],
    "techniciens-frigoristes": ["G1X74"],
    "techniciens-energie-renouvelable": ["G1X74"],
    # Transport et logistique
    "conducteurs-routiers": ["J3X43"],
    "livreurs": ["J3X42"],
    "conducteurs-bus": ["J3X41"],
    "conducteurs-train": ["J3X44"],
    "pilotes-avion": ["J6X91"],
    "magasiniers": ["J0X33", "J0X34"],
    "responsables-logistiques": ["J1X80", "J6X92"],
    "logisticiens": ["J5X80"],
    "agents-transit": ["J5X40a"],
    "declarants-douane": ["J4X62"],
    # Hôtellerie, restauration, tourisme
    "cuisiniers": ["S1X40"],
    "chefs-cuisine": ["S1X80"],
    "serveurs-restaurant": ["S2X61"],
    "receptionnistes-hotel": ["S2X60"],
    "agents-voyage": ["J4X63"],
    "guides-touristiques": ["J4X60"],
    # Agriculture et pêche
    "agriculteurs": ["A0X40"],
    "eleveurs": ["A0X41"],
    "ouvriers-viticoles": ["A1X42"],
    "jardiniers-paysagistes": ["A1X41"],
    "ingenieurs-agronomes": ["A2X90"],
    "veterinaires": ["V2X92"],
    "pecheurs": ["A3X40"],
    # Services à la personne
    "coiffeurs": ["T0X60a"],
    "estheticiens": ["T0X60b"],
    "assistants-maternels": ["T2B60a"],
    "aides-domicile": ["T1X60"],
    # Services à la collectivité
    "agents-securite": ["T3X61"],
    "agents-entretien": ["T4X60"],
    "agents-proprete-urbaine": ["T4X62a"],
    "sapeurs-pompiers": ["P4X60b"],
    "policiers": ["P4X60c"],
    "gendarmes": ["P4X60a"],
    "urbanistes": ["P2X90a"],
    "attaches-territoriaux": ["P2X90a"],
    "agents-impots": ["P1X80", "P2X90g"],
    "techniciens-traitement-eaux": ["G1X78"],
    # Social
    "educateurs-specialises": ["V4X83b"],
    "moniteurs-educateurs": ["V4X83b"],
    "assistants-service-social": ["V4X85c"],
    "animateurs-socioculturels": ["V5X81"],
    "conseillers-insertion": ["V4X80"],
    # Sport et loisirs
    "moniteurs-sport": ["V5X82"],
    "entraineurs-sportifs": ["V5X82"],
}

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _col(ref):
    n = 0
    for c in "".join(ch for ch in ref if ch.isalpha()):
        n = n * 26 + (ord(c) - 64)
    return n - 1


def read_xlsx(path):
    """Lecteur minimal : openpyxl échoue sur ces fichiers (relation drawing cassée)."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(f"{NS}si"):
            shared.append("".join(t.text or "" for t in si.iter(f"{NS}t")))
    rows = []
    for r in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(f"{NS}row"):
        cells = {}
        for c in r.findall(f"{NS}c"):
            v = c.find(f"{NS}v")
            if v is None:
                val = None
            elif c.get("t") == "s":
                val = shared[int(v.text)]
            else:
                try:
                    val = float(v.text)
                    if val == int(val):
                        val = int(val)
                except (TypeError, ValueError):
                    val = v.text
            cells[_col(c.get("r"))] = val
        rows.append([cells.get(i) for i in range(max(cells) + 1)] if cells else [])
    z.close()
    return rows


def remonte(table, fap):
    """FAP 341 -> FAP 228 -> FAP 86 tant que la valeur n'est pas publiée."""
    for code in (fap, fap[:5], fap[:3]):
        if table.get(code) is not None:
            return table[code], code
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="rapport seul, n'écrit pas metiers.csv")
    args = ap.parse_args()

    for f in (EFF_XLSX, SAL_XLSX):
        if not os.path.exists(f):
            raise SystemExit(f"{f} introuvable (voir README, section Sources de données).")

    eff_rows = read_xlsx(EFF_XLSX)[1:]
    effectifs = {r[1]: r[3] for r in eff_rows if r and r[0] == ANNEE_EFFECTIFS}
    libelles = {r[1]: r[2] for r in eff_rows if r}
    salaires = {r[0]: r[3] for r in read_xlsx(SAL_XLSX)[1:] if r and r[2] == PERIODE_SALAIRES}

    with open("metiers.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Combien de nos métiers partagent exactement la même liste de FAP ?
    partages = {}
    for slug, faps in FAP_MAP.items():
        partages.setdefault(tuple(sorted(faps)), []).append(slug)

    inconnus, sans_salaire, rapport = [], [], []

    for r in rows:
        slug = r["slug"]
        faps = FAP_MAP.get(slug)
        if not faps:
            inconnus.append(slug)
            continue

        n_partage = len(partages[tuple(sorted(faps))])
        total, poids, sal_src = 0, [], []
        for fap in faps:
            if fap not in effectifs:
                inconnus.append(f"{slug} -> code FAP inconnu {fap}")
                continue
            e = effectifs[fap]
            total += e
            s, src = remonte(salaires, fap)
            if s is not None:
                poids.append((e, s))
                sal_src.append(src)

        effectif = round(total / n_partage) if total else None
        salaire = round(sum(e * s for e, s in poids) / sum(e for e, _ in poids)) if poids else None
        if salaire is None:
            sans_salaire.append(slug)

        rapport.append({
            "slug": slug, "title": r["title"], "faps": faps, "n_partage": n_partage,
            "fap_labels": [libelles.get(f, "?") for f in faps],
            "effectif_total_fap": total or None, "effectif": effectif, "salaire_mensuel": salaire,
            "salaire_niveau": sorted(set(sal_src)),
            "ancien_effectif": int(r["nb_emplois"]) if r["nb_emplois"] else None,
            "ancien_salaire": int(r["salaire_median_mensuel"]) if r["salaire_median_mensuel"] else None,
        })

        r["nb_emplois"] = str(effectif) if effectif else ""
        r["salaire_median_mensuel"] = str(salaire) if salaire else ""
        r["salaire_median_annuel"] = str(salaire * 12) if salaire else ""

    with open(os.path.join(ED, "dares_stats_fr.json"), "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=1)

    if not args.dry_run:
        with open("metiers.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)

    couverts = [x for x in rapport if x["effectif"]]
    print(f"Métiers : {len(rows)} | rattachés à une FAP : {len(rapport)} | effectif disponible : {len(couverts)}")
    print(f"  salaire disponible : {len(rapport) - len(sans_salaire)}")
    print(f"  FAP distinctes utilisées : {len({f for x in rapport for f in x['faps']})}")
    multi = [x for x in rapport if x["n_partage"] > 1]
    print(f"  métiers partageant leur FAP (effectif réparti) : {len(multi)}")
    print(f"\n  Emploi total couvert : {sum(x['effectif'] for x in couverts):,}".replace(",", " "))
    anciens = [x["ancien_effectif"] for x in rapport if x["ancien_effectif"]]
    print(f"  (ancien total : {sum(anciens):,})".replace(",", " "))

    if inconnus:
        print(f"\nATTENTION, non traités ({len(inconnus)}) :")
        for x in inconnus:
            print(f"  - {x}")
    if sans_salaire:
        print(f"\nSans salaire publié ({len(sans_salaire)}) : {', '.join(sans_salaire)}")

    ecarts = sorted(
        (x for x in rapport if x["ancien_effectif"] and x["effectif"]),
        key=lambda x: -abs(x["effectif"] - x["ancien_effectif"]) / x["ancien_effectif"],
    )
    print("\n  Plus grands écarts d'effectif (nouveau vs ancien) :")
    for x in ecarts[:12]:
        d = (x["effectif"] - x["ancien_effectif"]) / x["ancien_effectif"] * 100
        print(f"    {x['slug']:36} {x['ancien_effectif']:>8} -> {x['effectif']:>8}  ({d:+.0f} %)")

    if args.dry_run:
        print("\n(dry-run : metiers.csv non modifié)")


if __name__ == "__main__":
    main()
