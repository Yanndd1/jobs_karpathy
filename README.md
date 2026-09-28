# Visualiseur du marché du travail français

Outil de recherche pour explorer visuellement les données du [répertoire ROME](https://candidat.francetravail.fr/metierscope/) de France Travail (anciennement Pôle Emploi). Ce n'est pas un rapport ni une publication scientifique — c'est un outil de développement pour explorer les données de l'emploi visuellement.

Fork de [karpathy/jobs](https://github.com/karpathy/jobs) adapté au marché du travail français.

## Contenu

Le répertoire ROME couvre les métiers de l'économie française avec des données détaillées sur les tâches, l'environnement de travail, les conditions d'accès, les compétences et les salaires. Nous avons scrappé ces données via l'API France Travail et construit une visualisation interactive en treemap où la **surface** de chaque rectangle est proportionnelle au nombre d'emplois et la **couleur** indique la métrique sélectionnée — basculez entre perspectives de croissance, salaire médian, niveau de formation et exposition à l'IA.

## D'où vient le score d'exposition

Contrairement au projet original, qui fait scorer chaque métier par un LLM, cette version agrège des travaux
académiques et institutionnels (OIT, Stanford, INSEE, France Stratégie) pondérés par niveau de preuve et par
récence, via le corpus de transitions-ia.fr. 124 métiers sont rattachés à ce corpus, 23 reposent sur une
estimation d'expert écrite à la main dans `build_scores.py`. Le pipeline de scoring par LLM du projet
original (`score.py`) est conservé dans le dépôt mais n'alimente plus le site.

**Ce que l'« Exposition IA » n'est PAS :**
- Elle ne prédit **pas** la disparition d'un métier. Les développeurs scorent 8/10 car l'IA transforme leur travail, mais la demande de logiciels pourrait facilement *augmenter*.
- Elle ne tient **pas** compte de l'élasticité de la demande, des barrières réglementaires, ou des préférences sociales.
- Ce sont des estimations, pas des prédictions rigoureuses.

## Pipeline de données

1. **Scraper** (`scrape_francetravail.py`) — Récupère les données via l'API France Travail (ROME v2) avec authentification OAuth2. Sauvegarde les JSON bruts dans `html/`.
2. **Parser** (`parse_rome.py`, `process.py`) — Convertit les données JSON/HTML en fichiers Markdown propres dans `pages/`.
3. **Tabuler** (`make_csv_fr.py`) — Extrait les champs structurés (salaire, formation, emplois, code ROME) dans `metiers.csv`.
3 bis. **Rafraîchir les statistiques** (`refresh_stats_fr.py`) : remplace les effectifs et les salaires de `metiers.csv` par ceux de la Dares (Portraits statistiques des métiers), via un rattachement des 147 métiers aux familles professionnelles FAP-2021. Option `--dry-run` pour un rapport sans écriture.
4. **Scorer** (`build_scores.py`) : rattache chaque métier au corpus multi-sources de transitions-ia.fr via `MANUAL_MAP` (124 métiers), ou applique une estimation d'expert écrite à la main via `MANUAL_SCORES` (23 métiers). Résultats dans `scores.json`. Le script `score.py` (scoring par LLM, hérité du projet original) n'est plus utilisé.
5. **Rapprocher l'exposition observée** (`build_observed_exposure.py`) : relie chaque métier à la profession SOC américaine la plus proche pour récupérer l'exposition observée de l'Anthropic Economic Index (mars 2026). Résultats dans `external_data/anthropic_observed_exposure_fr.json`.
6. **Construire les données du site** (`build_site_data.py`) : fusionne CSV, scores IA et exposition observée dans `site/data.json`.
7. **Site web** (`site/index.html`) : visualisation treemap interactive avec quatre couches : Perspectives, Salaire médian, Formation, Exposition IA.

## Fichiers clés

| Fichier | Description |
|---------|-------------|
| `metiers.json` | Liste principale des métiers avec titre, URL, catégorie, slug, code ROME |
| `metiers.csv` | Statistiques résumées : salaire, formation, nombre d'emplois |
| `scores.json` | Scores d'exposition IA (0-10) avec explications |
| `external_data/dares_psm_effectifs_2004_2024.xlsx` | Effectifs en emploi par famille professionnelle, 2004 à 2024 (Dares) |
| `external_data/dares_psm_salaire_median.xlsx` | Salaire mensuel net médian par famille professionnelle, 2023-2025 (Dares) |
| `external_data/dares_rome_to_fap2021.csv` | Table de passage Rome vers FAP-2021 (Dares) |
| `external_data/dares_stats_fr.json` | Rapport du rattachement de nos 147 métiers aux familles professionnelles |
| `external_data/anthropic_observed_exposure_2026_03.csv` | Exposition observée de 756 professions SOC (Anthropic Economic Index, mars 2026) |
| `external_data/anthropic_observed_exposure_fr.json` | Exposition observée rapprochée de nos 147 métiers (144 rapprochés) |
| `prompt.md` | Toutes les données dans un seul fichier, conçu pour être collé dans un LLM |
| `html/` | Données brutes de l'API France Travail (source de vérité) |
| `pages/` | Versions Markdown propres de chaque fiche métier |
| `site/` | Site web statique (visualisation treemap) |

## Prompt LLM

[`prompt.md`](prompt.md) package toutes les données — statistiques agrégées, répartitions par niveau, exposition par salaire/formation, et tous les métiers avec leurs scores et explications — dans un seul fichier conçu pour être collé dans un LLM. Régénérez-le avec `uv run python make_prompt.py`.

## Installation

```
uv sync
uv run playwright install chromium
```

Nécessite dans `.env` :
```
FRANCE_TRAVAIL_CLIENT_ID=votre_client_id
FRANCE_TRAVAIL_CLIENT_SECRET=votre_client_secret
OPENROUTER_API_KEY=votre_cle
```

## Utilisation

```bash
# Scraper les données France Travail (une seule fois, résultats mis en cache dans html/)
uv run python scrape_francetravail.py

# Générer le Markdown à partir des données brutes
uv run python process.py

# Générer le CSV résumé
uv run python make_csv_fr.py

# Rafraîchir effectifs et salaires depuis les données Dares
uv run python refresh_stats_fr.py

# Scorer l'exposition IA (rattachement au corpus multi-sources)
uv run python build_scores.py

# Rapprocher l'exposition observée (Anthropic Economic Index, mars 2026)
uv run python build_observed_exposure.py

# Construire les données du site
uv run python build_site_data.py

# Servir le site localement
cd site && python -m http.server 8000
```
