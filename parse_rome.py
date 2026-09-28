"""
Parse ROME occupation data (from France Travail API JSON or Métierscope HTML)
into clean Markdown documents.

Reads from html/<slug>.json (API data) or html/<slug>.html (web data).
Writes to pages/<slug>.md.

Usage:
    uv run python parse_rome.py html/developpeurs-informatiques.json
    uv run python parse_rome.py html/infirmiers-soins-generaux.html
"""

import sys
import re
import json
from bs4 import BeautifulSoup


def clean(text):
    """Clean up whitespace from extracted text."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_rome_json(json_path):
    """Parse a France Travail API JSON response into Markdown."""
    with open(json_path) as f:
        data = json.load(f)

    md = []

    # Title
    title = data.get("libelle", data.get("intitule", "Métier inconnu"))
    md.append(f"# {title}")
    md.append("")

    # ROME code
    code = data.get("code", data.get("codeRome", ""))
    if code:
        md.append(f"**Code ROME :** {code}")
        md.append("")

    # Definition / description
    definition = data.get("definition", "")
    if definition:
        md.append("## Définition")
        md.append("")
        md.append(definition)
        md.append("")

    # Access conditions
    acces = data.get("acces", data.get("conditionAcces", ""))
    if acces:
        md.append("## Conditions d'accès")
        md.append("")
        md.append(acces)
        md.append("")

    # Activities / tasks
    activites = data.get("activites", data.get("activitesPrincipales", []))
    if activites:
        md.append("## Activités principales")
        md.append("")
        if isinstance(activites, list):
            for act in activites:
                if isinstance(act, dict):
                    md.append(f"- {act.get('libelle', act.get('intitule', ''))}")
                else:
                    md.append(f"- {act}")
        elif isinstance(activites, str):
            md.append(activites)
        md.append("")

    # Competencies
    competences = data.get("competences", data.get("competencesPrincipales", []))
    if competences:
        md.append("## Compétences")
        md.append("")
        if isinstance(competences, list):
            for comp in competences:
                if isinstance(comp, dict):
                    label = comp.get("libelle", comp.get("intitule", ""))
                    type_comp = comp.get("type", "")
                    if type_comp:
                        md.append(f"- **{type_comp}** : {label}")
                    else:
                        md.append(f"- {label}")
                else:
                    md.append(f"- {comp}")
        md.append("")

    # Work environments
    contextes = data.get("contexteTravail", data.get("environnementsTravail", []))
    if contextes:
        md.append("## Environnements de travail")
        md.append("")
        if isinstance(contextes, list):
            for ctx in contextes:
                if isinstance(ctx, dict):
                    cat = ctx.get("categorie", ctx.get("libelle", ""))
                    vals = ctx.get("valeurs", [])
                    if vals:
                        md.append(f"### {cat}")
                        for v in vals:
                            if isinstance(v, dict):
                                md.append(f"- {v.get('libelle', '')}")
                            else:
                                md.append(f"- {v}")
                    else:
                        md.append(f"- {cat}")
                else:
                    md.append(f"- {ctx}")
        md.append("")

    # Appellations (specific job titles)
    appellations = data.get("appellations", [])
    if appellations:
        md.append("## Appellations courantes")
        md.append("")
        for app in appellations[:20]:  # Limit to top 20
            if isinstance(app, dict):
                md.append(f"- {app.get('libelle', app.get('intitule', ''))}")
            else:
                md.append(f"- {app}")
        if len(appellations) > 20:
            md.append(f"- ... et {len(appellations) - 20} autres")
        md.append("")

    # Mobility (related occupations)
    mobilites = data.get("mobilites", [])
    if mobilites:
        md.append("## Mobilités professionnelles")
        md.append("")
        for mob in mobilites[:10]:
            if isinstance(mob, dict):
                code_mob = mob.get("codeRome", mob.get("code", ""))
                label_mob = mob.get("libelle", mob.get("intitule", ""))
                md.append(f"- {label_mob} ({code_mob})")
            else:
                md.append(f"- {mob}")
        md.append("")

    return "\n".join(md)


def parse_metierscope_html(html_path):
    """Parse a Métierscope web page into Markdown."""
    with open(html_path) as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    md = []

    # Title
    h1 = soup.find("h1")
    title = clean(h1.get_text()) if h1 else "Métier inconnu"
    md.append(f"# {title}")
    md.append("")

    # Source URL
    canonical = soup.find("link", rel="canonical")
    if canonical:
        md.append(f"**Source :** {canonical['href']}")
        md.append("")

    # Main content sections
    for section in soup.find_all(["section", "div"], class_=re.compile(r"metier|fiche|description")):
        h2 = section.find(["h2", "h3"])
        if h2:
            md.append(f"## {clean(h2.get_text())}")
            md.append("")

        for elem in section.children:
            if hasattr(elem, 'name'):
                if elem.name in ('h2', 'h3'):
                    continue
                if elem.name == 'p':
                    text = clean(elem.get_text())
                    if text:
                        md.append(text)
                        md.append("")
                elif elem.name == 'ul':
                    for li in elem.find_all("li"):
                        md.append(f"- {clean(li.get_text())}")
                    md.append("")

    return "\n".join(md)


def parse_metier(path):
    """Auto-detect format and parse."""
    if path.endswith(".json"):
        return parse_rome_json(path)
    elif path.endswith(".html"):
        return parse_metierscope_html(path)
    else:
        raise ValueError(f"Unknown file format: {path}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "html/developpeurs-informatiques.json"
    result = parse_metier(path)

    out_path = path.rsplit(".", 1)[0] + ".md"
    out_path = out_path.replace("html/", "pages/")
    with open(out_path, "w") as f:
        f.write(result)
    print(f"Written to {out_path}")
    print()
    print(result)
