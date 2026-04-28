"""
Build scores.json by mapping external AI exposure data to our 147 ROME occupations.

Sources (in priority order):
1. transitions-ia.fr — 97 French occupations with multi-source weighted scores (0-10)
2. Demirev ESCO scores — 3000+ ESCO occupations with AI exposure scores
3. Manual expert mapping for remaining occupations

Also enriches metiers.json entries with salary and employment data from transitions-ia.fr.

Usage:
    uv run python build_scores.py
"""

import csv
import json
import os
import re
from difflib import SequenceMatcher


def normalize(s):
    """Normalize a string for fuzzy matching."""
    s = s.lower().strip()
    s = re.sub(r'[éèêë]', 'e', s)
    s = re.sub(r'[àâä]', 'a', s)
    s = re.sub(r'[ùûü]', 'u', s)
    s = re.sub(r'[ôö]', 'o', s)
    s = re.sub(r'[îï]', 'i', s)
    s = re.sub(r'[ç]', 'c', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


# Manual mapping: our slug -> transitions-ia.fr label (for hard cases)
MANUAL_MAP = {
    "comptables": "Comptable",
    "developpeurs-informatiques": "Développeur logiciel",
    "infirmiers-soins-generaux": "Infirmier",
    "aides-soignants": "Aide-soignant",
    "enseignants-secondaire": "Professeur collège-lycée",
    "enseignants-primaire": "Professeur des écoles",
    "agents-securite": None,
    "electriciens-batiment": "Électricien bâtiment",
    "plombiers-chauffagistes": None,
    "conseillers-bancaires": "Conseiller bancaire",
    "journalistes": "Journaliste",
    "avocats": "Avocat",
    "medecins-generalistes": "Médecin généraliste",
    "pharmaciens": "Pharmacien",
    "architectes": "Architecte",
    "conducteurs-routiers": "Chauffeur routier",
    "macons": "Maçon",
    "cuisiniers": "Cuisinier",
    "data-analysts": "Data scientist",
    "designers-graphiques": "Graphiste",
    "traducteurs-interpretes": "Traducteur",
    "redacteurs-web": "Rédacteur web",
    "community-managers": "Community manager",
    "experts-comptables": "Comptable",
    "chefs-projets-informatiques": "Chef de projet IT",
    "ingenieurs-informatique": "Développeur logiciel",
    "gestionnaires-paie": "Gestionnaire paie & administration RH",
    "controleurs-gestion": "Contrôleur de gestion",
    "responsables-rh": "DRH",
    "responsables-marketing": "E-commerce manager",
    "analystes-financiers": "Analyste financier",
    "juristes-entreprise": "Juriste d'entreprise",
    "directeurs-financiers": "Directeur de projet / PMO",
    "directeurs-generaux": "Directeur de projet / PMO",
    "conducteurs-travaux": "Conducteur de travaux",
    "veterinaires": "Vétérinaire",
    "psychologues": "Psychologue clinicien",
    "kinesitherapeutes": "Kinésithérapeute",
    "sages-femmes": "Sage-femme",
    "chirurgiens-dentistes": "Chirurgien-dentiste",
    "educateurs-specialises": "Éducateur spécialisé",
    "policiers": "Policier",
    "notaires": "Notaire",
    "greffiers": "Greffier",
    "coiffeurs": "Coiffeur-esthéticien",
    "mecaniciens-automobiles": "Mécanicien automobile",
    "soudeurs": "Soudeur",
    "logisticiens": "Logisticien",
    "formateurs": "Formateur professionnel / responsable formation",
    "photographes": "Photographe professionnel (art / studio)",
    "pilotes-avion": "Pilote de ligne",
    "receptionnistes-hotel": "Réceptionniste hôtel",
    "musiciens": "Musicien",
    "comediens": "Comédien / acteur",
    "agriculteurs": "Agriculteur céréalier",
    "assistants-service-social": "Travailleur social / assistant de service social",
    "chercheurs": "Enseignant-chercheur",
    "webmasters": "Rédacteur web",
    "auditeurs-financiers": "Analyste risques",
    "charges-communication": "Attaché de presse-RP",
    "chefs-produit": "E-commerce manager",
    "operateurs-saisie": None,
    "televendeurs": None,
    "operateurs-centre-appels": None,
    "conducteurs-bus": None,
    "conducteurs-train": None,
    "serveurs-restaurant": None,
    "vendeurs-magasin": "Vendeur automobile",
    "secretaires": None,
    "assistants-direction": None,
    "boulangers-patissiers": "Cuisinier",
    "bouchers": "Cuisinier",
    "caissiers": None,
    "agents-accueil": "Réceptionniste hôtel",
    "sapeurs-pompiers": None,
    "gendarmes": "Policier",
    "agents-immobiliers": "Agent immobilier",
    "techniciens-maintenance-industrielle": "Technicien maintenance",
    "techniciens-support-informatique": "Chef de projet IT",
    "ingenieurs-btp": "Conducteur de travaux",
    "techniciens-qualite": "Ingénieur process",
    "ingenieurs-mecanique": "Ingénieur process",
    "ingenieurs-energie": "Ingénieur process",
    "ingenieurs-environnement": "Ingénieur process",
    "ingenieurs-agronomes": "Agriculteur céréalier",
    "experts-cybersecurite": "Développeur logiciel",
    "manipulateurs-radiologie": "Radiologue",
    "orthophonistes": "Kinésithérapeute",
    "ergotherapeutes": "Kinésithérapeute",
    "dieteticiens": "Pharmacien",
    "preparateurs-pharmacie": "Pharmacien",
    "techniciens-labo-medical": "Pharmacien",
    "opticiens-lunetiers": "Pharmacien",
    "moniteurs-educateurs": "Éducateur spécialisé",
    "animateurs-socioculturels": "Éducateur spécialisé",
    "assistants-maternels": "Aide à domicile",
    "aides-domicile": "Aide à domicile",
    "conseillers-insertion": "Conseiller d'orientation-psychologue",
    "huissiers-justice": "Commissaire de justice",
    "bibliothecaires": "Conservateur de musée / patrimoine",
    "attaches-territoriaux": None,
    "agents-impots": None,
    "agents-entretien": None,
    "commerciaux-terrain": "Commercial B2B",
    "traders": "Analyste financier",
    "gestionnaires-patrimoine": "Conseiller en gestion de patrimoine",
    "techniciens-audiovisuels": "Monteur-vidéaste",
    "techniciens-electronique": "Automaticien",
    "techniciens-telecoms": "Automaticien",
    "techniciens-frigoristes": "Technicien maintenance",
    "techniciens-energie-renouvelable": "Automaticien",
    "techniciens-traitement-eaux": "Technicien maintenance",
    "conducteurs-ligne-production": "Technicien CNC / conducteur de machines",
    "conducteurs-engins-chantier": None,
    "menuisiers": "Maçon",
    "charpentiers": "Maçon",
    "couvreurs": "Maçon",
    "carreleurs": "Maçon",
    "peintres-batiment": "Maçon",
    "chaudronniers": "Soudeur",
    "usineurs": "Technicien CNC / conducteur de machines",
    "carrossiers": "Mécanicien automobile",
    "mecaniciens-aeronautiques": "Mécanicien automobile",
    "jardiniers-paysagistes": None,
    "eleveurs": "Éleveur bovin",
    "ouvriers-viticoles": "Maraîcher",
    "pecheurs": None,
    "geometres-topographes": "Architecte",
    "urbanistes": "Architecte",
    "guides-touristiques": None,
    "agents-voyage": "Agent immobilier",
    "agents-transit": "Logisticien",
    "declarants-douane": "Logisticien",
    "magasiniers": "Logisticien",
    "livreurs": "Chauffeur routier",
    "ambulanciers": None,
    "directeurs-magasin": "Consultant en management",
    "responsables-logistiques": "Logisticien",
    "acheteurs": "Commercial B2B",
    "chefs-cuisine": "Cuisinier",
    "estheticiens": "Coiffeur-esthéticien",
    "entraineurs-sportifs": None,
    "moniteurs-sport": None,
    "agents-proprete-urbaine": None,
    "operateurs-production": "Technicien CNC / conducteur de machines",
    "administrateurs-systemes-reseaux": "Développeur logiciel",
    "agents-assurance": "Conseiller bancaire",
}

# Manual scores for occupations with no match in transitions-ia.fr
MANUAL_SCORES = {
    "agents-securite": (3, "Surveillance terrain et intervention physique limitent l'automatisation. La vidéosurveillance IA progresse mais ne remplace pas la présence humaine."),
    "plombiers-chauffagistes": (2, "Intervention physique en milieu non structuré. Diagnostic et réparation manuels. Forte pénurie de main-d'œuvre."),
    "operateurs-saisie": (10, "Traitement routinier d'information entièrement numérique. L'IA réalise déjà la majorité de ces tâches."),
    "televendeurs": (10, "Prospection téléphonique scriptée. Les chatbots et voicebots IA remplacent progressivement ce métier."),
    "operateurs-centre-appels": (9, "Traitement d'appels standardisés très exposé aux chatbots IA. Seuls les cas complexes nécessitent encore un humain."),
    "conducteurs-bus": (4, "Conduite autonome progresse mais le contexte urbain et la responsabilité des passagers maintiennent l'humain à moyen terme."),
    "conducteurs-train": (5, "Automatisation avancée (métro sans conducteur). Le réseau ferré classique évolue plus lentement."),
    "serveurs-restaurant": (2, "Service en salle requiert présence physique, adaptation et contact humain. Automatisation anecdotique hors restauration rapide."),
    "vendeurs-magasin": (4, "Caisses automatiques et commerce en ligne progressent. Le conseil personnalisé et l'expérience en boutique résistent."),
    "secretaires": (8, "Gestion d'agenda, courriers, tri de mails : très automatisable par les assistants IA. La coordination humaine complexe résiste."),
    "assistants-direction": (7, "Organisation et communication très exposées aux outils IA. Le rôle stratégique de filtrage et de coordination résiste."),
    "boulangers-patissiers": (1, "Artisanat manuel, savoir-faire tactile et créativité culinaire. Automatisation très limitée hors industrie."),
    "bouchers": (1, "Découpe manuelle, relation client et expertise produit. Automatisation industrielle existe mais pas en boutique."),
    "caissiers": (9, "Caisses automatiques et paiement sans contact en forte expansion. Métier en restructuration majeure."),
    "agents-accueil": (5, "Bornes interactives et chatbots progressent. L'accueil personnalisé et la gestion des situations complexes résistent."),
    "sapeurs-pompiers": (2, "Intervention d'urgence physique en milieu dangereux. L'IA assiste la détection d'incendie et la logistique sans remplacer l'intervention."),
    "attaches-territoriaux": (5, "Administration et rédaction de rapports exposées. La connaissance du terrain local et la médiation politique résistent."),
    "agents-impots": (7, "Contrôle fiscal et traitement de dossiers très automatisables. L'interprétation des situations complexes résiste."),
    "agents-entretien": (1, "Travail physique de nettoyage. Robots aspirateurs existent mais ne couvrent pas le spectre complet des tâches."),
    "conducteurs-engins-chantier": (3, "Conduite d'engins en milieu de chantier variable. La téléopération progresse mais le contexte imprévisible freine l'automatisation."),
    "jardiniers-paysagistes": (1, "Travail physique en extérieur, adaptation constante au terrain et au vivant. Exposition minimale."),
    "pecheurs": (2, "Travail physique en mer, conditions imprévisibles. La technologie assiste la navigation et la détection mais pas la pêche elle-même."),
    "guides-touristiques": (5, "Audioguides et visites virtuelles IA progressent. Le contact humain, l'improvisation et la narration vivante résistent."),
    "ambulanciers": (2, "Transport sanitaire et premiers soins requièrent une présence physique et une réactivité humaine."),
    "entraineurs-sportifs": (2, "Coaching physique, motivation et adaptation en temps réel. Les applications fitness IA assistent mais ne remplacent pas."),
    "moniteurs-sport": (2, "Enseignement physique et sécurité des pratiquants. Présence humaine indispensable."),
    "agents-proprete-urbaine": (1, "Travail physique en extérieur, conditions variables. Automatisation très limitée en milieu urbain."),
}


def main():
    # Load transitions-ia.fr scores
    with open("external_data/transitions_ia_scores.json") as f:
        tia_data = json.load(f)
    tia_by_label = {entry["label"]: entry for entry in tia_data}

    # Load ESCO scores for supplementary matching
    esco_scores = {}
    with open("external_data/scored_esco_occupations.csv") as f:
        for row in csv.DictReader(f):
            esco_scores[row["occupation_title"].lower()] = float(row["ai_product_exposure_score"])

    # Load our metiers
    with open("metiers.json") as f:
        metiers = json.load(f)

    scores = []
    stats_enrichment = {}
    matched = 0
    manual = 0
    auto_fuzzy = 0
    manual_score = 0

    for m in metiers:
        slug = m["slug"]
        title = m["title"]
        entry = None
        source = ""

        # 1. Try manual mapping
        if slug in MANUAL_MAP and MANUAL_MAP[slug] is not None:
            mapped_label = MANUAL_MAP[slug]
            if mapped_label in tia_by_label:
                entry = tia_by_label[mapped_label]
                source = "transitions-ia.fr (manual map)"
                manual += 1

        # 2. Try exact/fuzzy match on label
        if entry is None:
            best_score = 0
            best_entry = None
            for label, e in tia_by_label.items():
                sim = similarity(title, label)
                if sim > best_score:
                    best_score = sim
                    best_entry = e
            if best_score >= 0.6:
                entry = best_entry
                source = f"transitions-ia.fr (fuzzy {best_score:.2f})"
                auto_fuzzy += 1

        if entry:
            exposure = round(entry["weighted_score"])
            exposure_raw = entry["weighted_score"]
            rationale = entry.get("rationale", "")
            num_sources = len(entry.get("sources", []))
            regulations = entry.get("regulations", [])

            # Also store salary/employment for CSV enrichment
            stats_enrichment[slug] = {
                "salary_net_monthly": entry.get("salary_net_monthly"),
                "employment_count": entry.get("employment_count"),
            }

            scores.append({
                "slug": slug,
                "title": title,
                "exposure": exposure,
                "exposure_raw": round(exposure_raw, 2),
                "rationale": rationale,
                "source": source,
                "num_evidence_sources": num_sources,
                "regulations": "|".join(regulations) if isinstance(regulations, list) else regulations,
            })
            matched += 1

        elif slug in MANUAL_SCORES:
            exp, rat = MANUAL_SCORES[slug]
            scores.append({
                "slug": slug,
                "title": title,
                "exposure": exp,
                "exposure_raw": float(exp),
                "rationale": rat,
                "source": "expert estimate",
                "num_evidence_sources": 0,
                "regulations": "",
            })
            manual_score += 1

        else:
            print(f"  WARNING: No score for {slug} ({title})")

    # Save scores.json
    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)

    # Save stats enrichment for CSV update
    with open("external_data/stats_enrichment.json", "w") as f:
        json.dump(stats_enrichment, f, indent=2, ensure_ascii=False)

    print(f"\nScoring complete:")
    print(f"  Total metiers: {len(metiers)}")
    print(f"  Scored: {len(scores)}")
    print(f"    - Manual map to transitions-ia.fr: {manual}")
    print(f"    - Fuzzy match to transitions-ia.fr: {auto_fuzzy}")
    print(f"    - Expert manual scores: {manual_score}")
    print(f"  Missing: {len(metiers) - len(scores)}")

    # Summary stats
    vals = [s["exposure"] for s in scores]
    avg = sum(vals) / len(vals) if vals else 0
    print(f"\n  Average exposure: {avg:.1f}")
    print(f"  Min: {min(vals)}, Max: {max(vals)}")

    # Distribution
    dist = {}
    for v in vals:
        dist[v] = dist.get(v, 0) + 1
    print("\n  Distribution:")
    for k in sorted(dist):
        print(f"    {k}: {'█' * dist[k]} ({dist[k]})")


if __name__ == "__main__":
    main()
