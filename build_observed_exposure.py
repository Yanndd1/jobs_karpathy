"""
Rapproche l'« exposition observée » de l'Anthropic Economic Index (mars 2026)
de nos 147 métiers ROME.

Source : Anthropic, « Labor market impacts of AI: A new measure and early evidence »,
5 mars 2026. Jeu de données : Anthropic/EconomicIndex, labor_market_impacts/job_exposure.csv
(756 professions SOC 2018, score 0-1).

Ce que mesure l'indicateur : la part des tâches d'une profession effectivement observée
dans l'usage réel de Claude, pondérée en faveur des usages d'automatisation. C'est une
mesure d'usage constaté, pas de potentiel théorique : elle est donc complémentaire du
score d'exposition 0-10 du projet, et ne le remplace pas.

Limite assumée : la correspondance métier français -> profession SOC américaine est
établie à la main (table SOC_MAP ci-dessous), profession par profession. Elle est
approximative par construction et auditable ligne à ligne. Les métiers sans équivalent
SOC propre dans le jeu de données restent à None.

Usage :
    uv run python build_observed_exposure.py
"""

import csv
import json
import os

SOURCE_CSV = "external_data/anthropic_observed_exposure_2026_03.csv"
OUTPUT_JSON = "external_data/anthropic_observed_exposure_fr.json"

# Notre slug -> code SOC 2018 de la profession américaine la plus proche.
# None = pas d'équivalent satisfaisant dans le jeu de données Anthropic.
SOC_MAP = {
    # Support entreprise / gestion
    "comptables": "13-2011",
    "experts-comptables": "13-2011",
    "auditeurs-financiers": "13-2011",
    "controleurs-gestion": "13-2031",
    "gestionnaires-paie": "43-3051",
    "secretaires": "43-6014",
    "assistants-direction": "43-6011",
    "agents-accueil": "43-4171",
    "operateurs-saisie": "43-9021",
    "responsables-rh": "11-3121",
    "acheteurs": "11-3061",
    # Informatique et télécoms
    "developpeurs-informatiques": "15-1252",
    "ingenieurs-informatique": "15-1252",
    "administrateurs-systemes-reseaux": "15-1244",
    "chefs-projets-informatiques": "11-3021",
    "data-analysts": "15-2051",
    "techniciens-support-informatique": "15-1232",
    "experts-cybersecurite": "15-1212",
    "techniciens-telecoms": "49-2022",
    "webmasters": "15-1254",
    # Santé
    "infirmiers-soins-generaux": "29-1141",
    "aides-soignants": "31-1131",
    "medecins-generalistes": "29-1215",
    "pharmaciens": "29-1051",
    "kinesitherapeutes": "29-1123",
    "chirurgiens-dentistes": "29-1021",
    "sages-femmes": "29-1161",
    "psychologues": "19-3033",
    "opticiens-lunetiers": "29-2081",
    "preparateurs-pharmacie": "29-2052",
    "ambulanciers": "53-3011",
    "manipulateurs-radiologie": "29-2034",
    "techniciens-labo-medical": "19-4021",
    "dieteticiens": "29-1031",
    "orthophonistes": "29-1127",
    "ergotherapeutes": "29-1122",
    # Enseignement, formation, recherche
    "enseignants-secondaire": "25-2031",
    "enseignants-primaire": "25-2021",
    "formateurs": "13-1151",
    "bibliothecaires": "25-4022",
    "chercheurs": None,  # pas de profession SOC « chercheur » générique
    # Droit et justice
    "avocats": "23-1011",
    "notaires": "23-1011",
    "juristes-entreprise": "23-1011",
    "huissiers-justice": "33-3011",
    "greffiers": "43-4031",
    # Banque, assurance, immobilier
    "agents-immobiliers": "41-9022",
    "conseillers-bancaires": "13-2072",
    "agents-assurance": "41-3021",
    "gestionnaires-patrimoine": "13-2052",
    "traders": "41-3031",
    "analystes-financiers": "13-2051",
    # Commerce et vente
    "vendeurs-magasin": "41-2031",
    "caissiers": "41-2011",
    "directeurs-magasin": "41-1011",
    "responsables-marketing": "11-2021",
    "commerciaux-terrain": "41-4012",
    "televendeurs": "41-9041",
    "operateurs-centre-appels": "43-4051",
    "chefs-produit": "13-1161",
    "boulangers-patissiers": "51-3011",
    "bouchers": "51-3021",
    # Communication et médias
    "designers-graphiques": "27-1024",
    "journalistes": "27-3023",
    "redacteurs-web": "27-3043",
    "charges-communication": "27-3031",
    "community-managers": "27-3031",
    "traducteurs-interpretes": "27-3091",
    "photographes": "27-4021",
    # Arts et spectacle
    "techniciens-audiovisuels": "27-4011",
    "comediens": "27-2011",
    "musiciens": "27-2042",
    # Direction d'entreprise
    "directeurs-generaux": "11-1011",
    "directeurs-financiers": "11-3031",
    # Construction et BTP
    "macons": "47-2021",
    "electriciens-batiment": "47-2111",
    "plombiers-chauffagistes": "47-2152",
    "peintres-batiment": "47-2141",
    "conducteurs-travaux": "47-1011",
    "charpentiers": "47-2031",
    "couvreurs": "47-2181",
    "carreleurs": "47-2044",
    "conducteurs-engins-chantier": "47-2073",
    "architectes": "17-1011",
    "geometres-topographes": "17-1022",
    "ingenieurs-btp": "17-2051",
    # Industrie
    "techniciens-maintenance-industrielle": "49-9041",
    "soudeurs": "51-4121",
    "operateurs-production": "51-9111",
    "ingenieurs-mecanique": "17-2141",
    "techniciens-qualite": "51-9061",
    "mecaniciens-automobiles": "49-3023",
    "carrossiers": "49-3021",
    "menuisiers": "47-2031",
    "techniciens-electronique": "17-3023",
    "mecaniciens-aeronautiques": "49-3011",
    "ingenieurs-energie": "17-2071",
    "techniciens-energie-renouvelable": "49-9081",
    "ingenieurs-environnement": "17-2081",
    "techniciens-frigoristes": "49-9021",
    "chaudronniers": "47-2011",
    "usineurs": "51-4041",
    "conducteurs-ligne-production": "51-4081",
    # Transport et logistique
    "conducteurs-routiers": "53-3032",
    "agents-transit": "43-5011",
    "magasiniers": "43-5071",
    "livreurs": "53-3033",
    "responsables-logistiques": "11-3071",
    "conducteurs-bus": "53-3052",
    "conducteurs-train": "53-4011",
    "pilotes-avion": "53-2011",
    "logisticiens": "13-1081",
    "declarants-douane": "13-1041",
    # Hôtellerie et restauration
    "cuisiniers": "35-2014",
    "serveurs-restaurant": "35-3031",
    "chefs-cuisine": "35-1011",
    "agents-voyage": "41-3041",
    "receptionnistes-hotel": "43-4081",
    "guides-touristiques": None,  # « Tour and Travel Guides » absent du jeu de données
    # Agriculture et pêche
    "agriculteurs": "11-9013",
    "jardiniers-paysagistes": "37-3011",
    "veterinaires": "29-1131",
    "ingenieurs-agronomes": "17-2021",
    "ouvriers-viticoles": "45-2092",
    "eleveurs": "11-9013",
    "pecheurs": None,  # « Fishing and Hunting Workers » absent du jeu de données
    # Services à la personne
    "coiffeurs": "39-5012",
    "estheticiens": "39-5094",
    "assistants-maternels": "39-9011",
    "aides-domicile": "31-1131",
    # Services à la collectivité
    "agents-securite": "33-9032",
    "agents-entretien": "37-2011",
    "sapeurs-pompiers": "33-2011",
    "policiers": "33-3051",
    "gendarmes": "33-3051",
    "agents-proprete-urbaine": "53-7081",
    "urbanistes": "19-3051",
    "agents-impots": "13-2081",
    "attaches-territoriaux": "11-9199",
    "techniciens-traitement-eaux": "51-8031",
    # Social
    "educateurs-specialises": "21-1021",
    "assistants-service-social": "21-1021",
    "animateurs-socioculturels": "39-9032",
    "conseillers-insertion": "21-1012",
    "moniteurs-educateurs": "21-1093",
    # Sport et loisirs
    "moniteurs-sport": "39-9031",
    "entraineurs-sportifs": "27-2022",
}


def main():
    if not os.path.exists(SOURCE_CSV):
        raise SystemExit(
            f"{SOURCE_CSV} introuvable. Télécharger depuis :\n"
            "https://huggingface.co/datasets/Anthropic/EconomicIndex/"
            "resolve/main/labor_market_impacts/job_exposure.csv"
        )

    with open(SOURCE_CSV, encoding="utf-8") as f:
        soc = {
            row["occ_code"]: (row["title"], float(row["observed_exposure"]))
            for row in csv.DictReader(f)
        }

    with open("metiers.json", encoding="utf-8") as f:
        metiers = json.load(f)

    result = {}
    missing_slugs = []
    unknown_codes = []

    for m in metiers:
        slug = m["slug"]
        if slug not in SOC_MAP:
            missing_slugs.append(slug)
            continue
        code = SOC_MAP[slug]
        if code is None:
            result[slug] = None
            continue
        if code not in soc:
            unknown_codes.append((slug, code))
            result[slug] = None
            continue
        title, value = soc[code]
        result[slug] = {
            "soc_code": code,
            "soc_title": title,
            "observed_exposure": round(value, 4),
        }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    mapped = sum(1 for v in result.values() if v)
    print(f"Métiers traités : {len(result)}/{len(metiers)}")
    print(f"  Rapprochés à une profession SOC : {mapped}")
    print(f"  Sans équivalent SOC : {len(result) - mapped}")

    if missing_slugs:
        print(f"\nATTENTION  :  slugs absents de SOC_MAP ({len(missing_slugs)}) :")
        for s in missing_slugs:
            print(f"  - {s}")
    if unknown_codes:
        print(f"\nATTENTION  :  codes SOC absents du jeu de données ({len(unknown_codes)}) :")
        for s, c in unknown_codes:
            print(f"  - {s} -> {c}")

    vals = [v["observed_exposure"] for v in result.values() if v]
    if vals:
        print(f"\nExposition observée, moyenne : {sum(vals) / len(vals):.3f}")
        print(f"  min {min(vals):.3f} / max {max(vals):.3f}")
        top = sorted(
            ((v["observed_exposure"], k) for k, v in result.items() if v), reverse=True
        )[:10]
        print("\n  Top 10 :")
        for value, slug in top:
            print(f"    {value:.3f}  {slug}")


if __name__ == "__main__":
    main()
