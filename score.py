"""
Score each occupation's AI exposure using an LLM via OpenRouter.

Reads Markdown descriptions from pages/, sends each to an LLM with a scoring
rubric adapted for the French labor market, and collects structured scores.
Results are cached incrementally to scores.json so the script can be resumed.

Usage:
    uv run python score.py
    uv run python score.py --model google/gemini-3-flash-preview
    uv run python score.py --start 0 --end 10   # test on first 10
"""

import argparse
import json
import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "google/gemini-3-flash-preview"
OUTPUT_FILE = "scores.json"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """\
Vous êtes un analyste expert évaluant l'exposition des différents métiers \
à l'intelligence artificielle dans le contexte du marché du travail français. \
On vous fournira une description détaillée d'un métier issu du répertoire ROME \
(Répertoire Opérationnel des Métiers et des Emplois) de France Travail.

Évaluez l'**Exposition à l'IA** de ce métier sur une échelle de 0 à 10.

L'Exposition à l'IA mesure : dans quelle mesure l'IA va-t-elle transformer \
ce métier ? Considérez à la fois les effets directs (l'IA automatisant des \
tâches actuellement réalisées par des humains) et les effets indirects (l'IA \
rendant chaque travailleur si productif que moins de personnes sont nécessaires).

Un signal clé est de savoir si le produit du travail est fondamentalement \
numérique. Si le métier peut être exercé entièrement depuis un bureau à \
domicile sur un ordinateur — écrire, coder, analyser, communiquer — alors \
l'exposition à l'IA est intrinsèquement élevée (7+), car les capacités de \
l'IA dans les domaines numériques progressent rapidement. Même si l'IA \
actuelle ne peut pas gérer tous les aspects d'un tel métier, la trajectoire \
est forte et le plafond très haut. À l'inverse, les métiers nécessitant une \
présence physique, un savoir-faire manuel ou une interaction humaine en temps \
réel dans le monde physique ont une barrière naturelle à l'exposition à l'IA.

Tenez compte des spécificités françaises :
- Le cadre réglementaire français et européen (RGPD, AI Act) peut freiner \
certaines applications de l'IA
- La place de la fonction publique et des services publics en France
- Les conventions collectives et le droit du travail français
- La structure du tissu économique français (PME/TPE, artisanat, etc.)
- Les métiers réglementés (professions libérales, métiers de santé, etc.)

Utilisez ces repères pour calibrer votre score :

- **0–1 : Exposition minimale.** Le travail est presque entièrement physique, \
manuel, ou nécessite une présence humaine en temps réel dans des environnements \
imprévisibles. L'IA n'a essentiellement aucun impact sur le travail quotidien. \
Exemples : couvreur, jardinier-paysagiste, maçon.

- **2–3 : Exposition faible.** Travail principalement physique ou \
interpersonnel. L'IA peut aider sur des tâches périphériques mineures \
(planification, administratif) mais ne touche pas le cœur du métier. \
Exemples : électricien, plombier, sapeur-pompier, aide-soignant.

- **4–5 : Exposition modérée.** Un mélange de travail physique/interpersonnel \
et de travail intellectuel. L'IA peut aider significativement sur les parties \
liées au traitement de l'information, mais une part substantielle du métier \
nécessite encore une présence humaine. \
Exemples : infirmier, policier, vétérinaire, éducateur spécialisé.

- **6–7 : Exposition élevée.** Travail principalement intellectuel avec \
un certain besoin de jugement humain, de relations ou de présence physique. \
Les outils d'IA sont déjà utiles et les travailleurs utilisant l'IA peuvent \
être substantiellement plus productifs. \
Exemples : enseignant, comptable, journaliste, conseiller bancaire.

- **8–9 : Exposition très élevée.** Le métier s'exerce presque entièrement \
sur ordinateur. Toutes les tâches principales — écrire, coder, analyser, \
concevoir, communiquer — sont dans des domaines où l'IA progresse rapidement. \
Le métier fait face à une restructuration majeure. \
Exemples : développeur informatique, designer graphique, traducteur, \
data analyst, rédacteur web, gestionnaire de paie.

- **10 : Exposition maximale.** Traitement routinier d'informations, \
entièrement numérique, sans composante physique. L'IA peut déjà réaliser \
la plupart des tâches aujourd'hui. \
Exemples : opérateur de saisie, télévendeur.

Répondez avec UNIQUEMENT un objet JSON dans ce format exact, sans autre texte :
{
  "exposure": <0-10>,
  "rationale": "<2-3 phrases en français expliquant les facteurs clés>"
}\
"""


def score_occupation(client, text, model):
    """Send one occupation to the LLM and parse the structured response."""
    response = client.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]

    # Strip markdown code fences if present
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1]  # remove first line
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    return json.loads(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--force", action="store_true",
                        help="Re-score even if already cached")
    args = parser.parse_args()

    with open("metiers.json") as f:
        metiers = json.load(f)

    subset = metiers[args.start:args.end]

    # Load existing scores
    scores = {}
    if os.path.exists(OUTPUT_FILE) and not args.force:
        with open(OUTPUT_FILE) as f:
            for entry in json.load(f):
                scores[entry["slug"]] = entry

    print(f"Scoring {len(subset)} métiers avec {args.model}")
    print(f"Déjà en cache : {len(scores)}")

    errors = []
    client = httpx.Client()

    for i, m in enumerate(subset):
        slug = m["slug"]

        if slug in scores:
            continue

        md_path = f"pages/{slug}.md"
        if not os.path.exists(md_path):
            print(f"  [{i+1}] SKIP {slug} (pas de markdown)")
            continue

        with open(md_path) as f:
            text = f.read()

        print(f"  [{i+1}/{len(subset)}] {m['title']}...", end=" ", flush=True)

        try:
            result = score_occupation(client, text, args.model)
            scores[slug] = {
                "slug": slug,
                "title": m["title"],
                **result,
            }
            print(f"exposition={result['exposure']}")
        except Exception as e:
            print(f"ERREUR: {e}")
            errors.append(slug)

        # Save after each one (incremental checkpoint)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(list(scores.values()), f, indent=2, ensure_ascii=False)

        if i < len(subset) - 1:
            time.sleep(args.delay)

    client.close()

    print(f"\nTerminé. {len(scores)} métiers scorés, {len(errors)} erreurs.")
    if errors:
        print(f"Erreurs : {errors}")

    # Summary stats
    vals = [s for s in scores.values() if "exposure" in s]
    if vals:
        avg = sum(s["exposure"] for s in vals) / len(vals)
        by_score = {}
        for s in vals:
            bucket = s["exposure"]
            by_score[bucket] = by_score.get(bucket, 0) + 1
        print(f"\nExposition moyenne sur {len(vals)} métiers : {avg:.1f}")
        print("Distribution :")
        for k in sorted(by_score):
            print(f"  {k}: {'█' * by_score[k]} ({by_score[k]})")


if __name__ == "__main__":
    main()
