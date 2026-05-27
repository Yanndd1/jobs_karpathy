# Visualiseur du marché du travail français

Outil de recherche pour explorer visuellement les données du [répertoire ROME](https://candidat.francetravail.fr/metierscope/) de France Travail (anciennement Pôle Emploi). Ce n'est pas un rapport ni une publication scientifique — c'est un outil de développement pour explorer les données de l'emploi visuellement.

Fork de [karpathy/jobs](https://github.com/karpathy/jobs) adapté au marché du travail français.

## Contenu

Le répertoire ROME couvre les métiers de l'économie française avec des données détaillées sur les tâches, l'environnement de travail, les conditions d'accès, les compétences et les salaires. Nous avons scrappé ces données via l'API France Travail et construit une visualisation interactive en treemap où la **surface** de chaque rectangle est proportionnelle au nombre d'emplois et la **couleur** indique la métrique sélectionnée — basculez entre perspectives de croissance, salaire médian, niveau de formation et exposition à l'IA.

## Coloration par LLM

Le repo inclut des scrapers, des parsers et un pipeline pour écrire des prompts LLM personnalisés afin de scorer et colorer les métiers selon n'importe quel critère. Vous écrivez un prompt, le LLM score chaque métier, et le treemap colore en conséquence. L'option « Exposition IA » en est un exemple — elle estime dans quelle mesure l'IA actuelle (principalement numérique) va transformer chaque métier. Voir `score.py` pour le prompt et le pipeline de scoring.

**Ce que l'« Exposition IA » n'est PAS :**
- Elle ne prédit **pas** la disparition d'un métier. Les développeurs scorent 9/10 car l'IA transforme leur travail — mais la demande de logiciels pourrait facilement *augmenter*.
- Elle ne tient **pas** compte de l'élasticité de la demande, des barrières réglementaires, ou des préférences sociales.
- Les scores sont des estimations brutes d'un LLM (Gemini Flash via OpenRouter), pas des prédictions rigoureuses.

## Pipeline de données

1. **Scraper** (`scrape_francetravail.py`) — Récupère les données via l'API France Travail (ROME v2) avec authentification OAuth2. Sauvegarde les JSON bruts dans `html/`.
2. **Parser** (`parse_rome.py`, `process.py`) — Convertit les données JSON/HTML en fichiers Markdown propres dans `pages/`.
3. **Tabuler** (`make_csv_fr.py`) — Extrait les champs structurés (salaire, formation, emplois, code ROME) dans `metiers.csv`.
4. **Scorer** (`score.py`) — Envoie la description Markdown de chaque métier à un LLM avec un rubrique de scoring adapté au contexte français. Résultats dans `scores.json`.
5. **Construire les données du site** (`build_site_data.py`) — Fusionne CSV et scores IA dans `site/data.json`.
6. **Site web** (`site/index.html`) — Visualisation treemap interactive avec quatre couches : Perspectives, Salaire médian, Formation, Exposition IA.

## Fichiers clés

| Fichier | Description |
|---------|-------------|
| `metiers.json` | Liste principale des métiers avec titre, URL, catégorie, slug, code ROME |
| `metiers.csv` | Statistiques résumées : salaire, formation, nombre d'emplois |
| `scores.json` | Scores d'exposition IA (0-10) avec explications |
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

# Scorer l'exposition IA (utilise l'API OpenRouter)
uv run python score.py

# Construire les données du site
uv run python build_site_data.py

# Servir le site localement
cd site && python -m http.server 8000
```
