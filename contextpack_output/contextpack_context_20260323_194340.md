# 📦 ContextPack — contextpack

> Généré le 23/03/2026 à 19:43 par ContextPack
> 8 fichiers • 46.5 Ko total

---

# 🧠 Résumé de contexte — Généré par ContextPack

## 📋 Type de projet détecté
Projet **Python** (package)

## 📊 Vue d'ensemble
- **8 fichiers** inclus dans ce pack
- **~12,166 tokens** estimés au total

## 📁 Fichiers clés
- `README.md` — Documentation principale
- `pyproject.toml` — Configuration Python

## 📂 Arborescence complète
```
📄 .contextpack.yml
📄 README.md
📁 contextpack/
  📄 cli.py
  📄 config.py
  📄 exporter.py
  📄 scanner.py
  📄 summarizer.py
📄 pyproject.toml
```

---
*Résumé généré en mode local (sans API). Pour un résumé IA complet, utilise `--summary api`.*

---

## 📚 Table des matières

1. [README.md](#readmemd)
2. [.contextpack.yml](#contextpackyml)
3. [contextpack\cli.py](#contextpack\clipy)
4. [contextpack\config.py](#contextpack\configpy)
5. [contextpack\exporter.py](#contextpack\exporterpy)
6. [contextpack\scanner.py](#contextpack\scannerpy)
7. [contextpack\summarizer.py](#contextpack\summarizerpy)
8. [pyproject.toml](#pyprojecttoml)

---

## `README.md`
*Taille: 3.5 Ko • ~1,021 tokens • markdown*

```markdown
# 🧠 ContextPack

> **Reprends n'importe quel projet IA en 30 secondes après expiration du contexte.**

Quand le contexte d'une conversation IA expire, tu perds tout le fil. ContextPack génère automatiquement un **pack de reprise** — un PDF ou Markdown consolidé avec tous tes fichiers + un résumé IA — prêt à coller dans une nouvelle conversation.

---

## ✨ Fonctionnalités

- 📁 **Scan intelligent** — Détecte automatiquement les fichiers pertinents, respecte `.gitignore`
- 🤖 **Résumé IA** — Via API Anthropic Claude ou génération locale (sans API)
- 📄 **Export PDF** — Document paginé avec table des matières, header/footer, coloration
- 📝 **Export Markdown** — Fichier unique consolidé, parfait à coller dans une conversation
- 🔢 **Estimation tokens** — Sais exactement combien de tokens ton pack va consommer
- 🔍 **Mode diff** — Vois quels fichiers ont changé depuis le dernier pack
- ⚙️ **Config YAML** — Personnalise includes/excludes par projet

---

## 🚀 Installation

```bash
pip install contextpack
```

Ou depuis les sources :
```bash
git clone https://github.com/RadjTech/contextpack.git
cd contextpack
pip install -e .
```

---

## 📖 Usage

### Commande principale

```bash
# Pack simple (PDF + Markdown + résumé local)
contextpack pack

# Avec résumé IA via API
contextpack pack --summary api --api-key sk-ant-...

# Ou via variable d'environnement (recommandé)
export ANTHROPIC_API_KEY=sk-ant-...
contextpack pack --summary api

# PDF seulement, max 3 pages par fichier
contextpack pack --no-markdown --max-pages 3

# Seulement les fichiers modifiés depuis le dernier commit git
contextpack pack --since-git

# Résumé en anglais
contextpack pack --lang en

# Dossier de sortie personnalisé
contextpack pack -o ~/Desktop/mon_pack
```

### Initialiser la config

```bash
contextpack init
# Crée .contextpack.yml dans le dossier courant
```

### Voir les fichiers modifiés

```bash
contextpack diff
# Montre ce qui a changé depuis le dernier pack
```

---

## ⚙️ Configuration `.contextpack.yml`

```yaml
# Fichiers à inclure
include:
  - "**/*.py"
  - "**/*.ts"
  - "**/*.md"
  - "**/*.toml"

# Fichiers à exclure
exclude:
  - "**/node_modules/**"
  - "**/__pycache__/**"
  - "**/*.lock"
  - "**/dist/**"

# Taille max par fichier (Ko)
max_file_size_kb: 500

# Nombre max de pages PDF par fichier
max_pages_per_file: 5

# Mode résumé: "api" | "local" | "none"
summary_mode: "local"

# Langue du résumé
language: "fr"

# Formats de sortie
output_formats:
  - pdf
  - markdown
```

---

## 🔑 Modes de résumé IA

| Mode | Description | Qualité | Coût |
|------|-------------|---------|------|
| `api` | Claude analyse ton code via l'API Anthropic | ⭐⭐⭐⭐⭐ | Quelques centimes |
| `local` | Heuristique locale (sans API) | ⭐⭐⭐ | Gratuit |
| `none` | Pas de résumé, juste les fichiers | — | Gratuit |

---

## 💬 Prompt de reprise suggéré

Après avoir généré ton pack, colle ce message dans ta nouvelle conversation :

```
Voici mon projet [NOM]. Je te fournis le fichier contextpack qui contient 
tous les fichiers et le résumé de là où on en était. Analyse-le et reprends le travail.
[Attache le PDF ou colle le contenu Markdown]
```

---

## 📦 Dépendances

- `typer` + `rich` — CLI élégante
- `reportlab` — Génération PDF
- `tiktoken` — Estimation tokens
- `anthropic` — API Claude (optionnel)
- `pyyaml` — Config YAML
- `pathspec` — Patterns `.gitignore`

---

## 📄 Licence

MIT — Utilise librement, contribue si tu veux !

```

---

## `.contextpack.yml`
*Taille: 0.9 Ko • ~295 tokens • yaml*

```yaml
# ContextPack Configuration
# Documentation: https://github.com/contextpack/contextpack

# Fichiers à inclure (glob patterns)
include:
  - "**/*.py"
  - "**/contextpack/**"
  - "**/*.md"
  - "**/*.toml"
  - "**/*.yml"


# Fichiers/dossiers à exclure
exclude:
  - "**/__pycache__/**"
  - "**/*.pyc"
  - "**/node_modules/**"
  - "**/.git/**"
  - "**/dist/**"
  - "**/build/**"
  - "**/.venv/**"
  - "**/venv/**"
  - "**/*.lock"
  - "**/*.log"
  - "**/contextpack_output/**"
  - "**/*.min.js"
  - "**/*.min.css"

# Taille max par fichier (en Ko)
max_file_size_kb: 500

# Nombre max de pages PDF par fichier
max_pages_per_file: 5

# Mode résumé IA: "api" | "local" | "none"
summary_mode: "local"

# Clé API Anthropic (optionnel, préférer variable d'env ANTHROPIC_API_KEY)
# api_key: "sk-ant-..."

# Langue du résumé
language: "fr"

# Formats de sortie
output_formats:
  - pdf
  - markdown

```

---

## `contextpack\cli.py`
*Taille: 7.4 Ko • ~1,977 tokens • python*

```python
"""
ContextPack — CLI de sauvegarde de contexte IA
Reprends n'importe quel projet en 30 secondes après expiration du contexte.
"""

import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .scanner import scan_project
from .exporter import export_markdown, export_pdf
from .summarizer import generate_summary, generate_summary_local
from .config import load_config, create_default_config, Config

app = typer.Typer(
    name="contextpack",
    help="🧠 ContextPack — Sauvegarde ton contexte IA en un seul fichier.",
    add_completion=False,
)
console = Console()


def print_banner():
    text = Text()
    text.append("🧠 ContextPack", style="bold cyan")
    text.append(" — Reprends là où tu t'es arrêté\n", style="dim white")
    console.print(Panel(text, border_style="cyan", padding=(0, 2)))


@app.command("init")
def cmd_init(
    path: Path = typer.Argument(Path("."), help="Répertoire du projet"),
):
    """Initialise un fichier .contextpack.yml dans le projet."""
    print_banner()
    config_file = path / ".contextpack.yml"
    if config_file.exists():
        overwrite = typer.confirm("⚠️  .contextpack.yml existe déjà. Écraser ?")
        if not overwrite:
            raise typer.Exit()
    create_default_config(config_file)
    console.print(f"[green]✅ Fichier de config créé :[/green] {config_file}")
    console.print("[dim]Édite .contextpack.yml pour personnaliser les fichiers inclus/exclus.[/dim]")


@app.command("pack")
def cmd_pack(
    path: Path = typer.Argument(Path("."), help="Répertoire du projet"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Dossier de sortie (défaut: ./contextpack_output)"),
    pdf: bool = typer.Option(True, "--pdf/--no-pdf", help="Générer le PDF"),
    markdown: bool = typer.Option(True, "--markdown/--no-markdown", help="Générer le Markdown"),
    summary: Optional[str] = typer.Option(None, "--summary", "-s", help="Mode résumé IA: 'api' | 'local' | 'none'"),
    api_key: Optional[str] = typer.Option(None, "--api-key", envvar="ANTHROPIC_API_KEY", help="Clé API Anthropic"),
    max_pages: int = typer.Option(5, "--max-pages", "-p", help="Nombre max de pages PDF par fichier"),
    since_git: bool = typer.Option(False, "--since-git", help="Inclure seulement les fichiers modifiés depuis le dernier commit"),
    language: str = typer.Option("fr", "--lang", "-l", help="Langue du résumé (fr, en, ...)"),
    estimate_tokens: bool = typer.Option(True, "--tokens/--no-tokens", help="Estimer les tokens"),
):
    """
    📦 Génère un pack de contexte complet du projet.

    Exemples:\n
        contextpack pack\n
        contextpack pack --summary api --api-key sk-...\n
        contextpack pack --no-pdf --summary local\n
        contextpack pack --since-git --max-pages 3
    """
    print_banner()

    # Charger la config
    config = load_config(path)

    # Dossier de sortie
    out_dir = output or (path / "contextpack_output")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Scanner
    console.print("\n[bold cyan]📁 Scan du projet...[/bold cyan]")
    files = scan_project(path, config, since_git=since_git, estimate_tokens=estimate_tokens)

    if not files:
        console.print("[red]❌ Aucun fichier trouvé. Vérifie ta config .contextpack.yml[/red]")
        raise typer.Exit(1)

    console.print(f"[green]✅ {len(files)} fichiers trouvés[/green]")

    # Résumé IA
    summary_text = ""
    summary_mode = summary or config.summary_mode

    if summary_mode and summary_mode != "none":
        console.print(f"\n[bold cyan]🤖 Génération du résumé IA (mode: {summary_mode})...[/bold cyan]")
        try:
            if summary_mode == "api":
                key = api_key or config.api_key
                if not key:
                    console.print("[yellow]⚠️  Pas de clé API. Fallback vers résumé local.[/yellow]")
                    summary_text = generate_summary_local(files, language)
                else:
                    summary_text = generate_summary(files, language=language, api_key=key)
            else:  # local
                summary_text = generate_summary_local(files, language)
            console.print("[green]✅ Résumé généré[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Erreur résumé: {e}. Passage sans résumé.[/yellow]")

    # Export Markdown
    if markdown:
        console.print("\n[bold cyan]📝 Export Markdown...[/bold cyan]")
        md_path = export_markdown(files, out_dir, summary_text, path)
        console.print(f"[green]✅ Markdown :[/green] {md_path}")

    # Export PDF
    if pdf:
        console.print("\n[bold cyan]📄 Export PDF...[/bold cyan]")
        pdf_path = export_pdf(files, out_dir, summary_text, path, max_pages_per_file=max_pages)
        console.print(f"[green]✅ PDF :[/green] {pdf_path}")

    # Résumé final
    total_size = sum(f["size"] for f in files)
    total_tokens = sum(f.get("tokens", 0) for f in files)

    console.print(Panel(
        f"[bold green]Pack généré avec succès ![/bold green]\n\n"
        f"  📂 Fichiers   : [cyan]{len(files)}[/cyan]\n"
        f"  📦 Taille     : [cyan]{total_size / 1024:.1f} Ko[/cyan]\n"
        f"  🔢 Tokens est.: [cyan]{total_tokens:,}[/cyan]\n"
        f"  📁 Sortie     : [cyan]{out_dir}[/cyan]",
        border_style="green",
        title="✅ Résultat",
    ))

    # Prompt de reprise suggéré
    project_name = path.resolve().name
    console.print(Panel(
        f'[dim]Colle ce message en début de nouvelle conversation :\n\n[/dim]'
        f'[italic]"Voici mon projet [bold]{project_name}[/bold]. '
        f'Je te fournis le fichier contextpack qui contient tous les fichiers et le résumé de là où on en était. '
        f'Analyse-le et reprends le travail."[/italic]',
        border_style="yellow",
        title="💬 Prompt de reprise suggéré",
        padding=(1, 2),
    ))


@app.command("diff")
def cmd_diff(
    path: Path = typer.Argument(Path("."), help="Répertoire du projet"),
):
    """🔍 Affiche les fichiers modifiés depuis le dernier pack."""
    print_banner()
    import subprocess
    from datetime import datetime

    out_dir = path / "contextpack_output"
    last_pack = None

    if out_dir.exists():
        packs = sorted(out_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        if packs:
            last_pack = packs[0]

    if not last_pack:
        console.print("[yellow]Aucun pack précédent trouvé. Lance 'contextpack pack' d'abord.[/yellow]")
        raise typer.Exit()

    pack_time = last_pack.stat().st_mtime
    pack_dt = datetime.fromtimestamp(pack_time)
    console.print(f"[dim]Dernier pack: {pack_dt.strftime('%d/%m/%Y %H:%M')}[/dim]\n")

    config = load_config(path)
    files = scan_project(path, config)

    changed = [f for f in files if f["mtime"] > pack_time]
    unchanged = [f for f in files if f["mtime"] <= pack_time]

    if changed:
        console.print(f"[bold yellow]📝 {len(changed)} fichier(s) modifié(s) depuis le dernier pack:[/bold yellow]")
        for f in changed:
            console.print(f"  [yellow]~[/yellow] {f['rel_path']}")
    else:
        console.print("[green]✅ Aucun fichier modifié depuis le dernier pack.[/green]")

    console.print(f"\n[dim]{len(unchanged)} fichiers inchangés[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()

```

---

## `contextpack\config.py`
*Taille: 3.1 Ko • ~917 tokens • python*

```python
"""Gestion de la configuration .contextpack.yml"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import yaml


@dataclass
class Config:
    include: List[str] = field(default_factory=lambda: [
        "**/*.py", "**/*.js", "**/*.ts", "**/*.tsx", "**/*.jsx",
        "**/*.go", "**/*.rs", "**/*.java", "**/*.c", "**/*.cpp",
        "**/*.md", "**/*.txt", "**/*.toml", "**/*.yaml", "**/*.yml",
        "**/*.json", "**/*.env.example", "**/*.sh",
    ])
    exclude: List[str] = field(default_factory=lambda: [
        "**/__pycache__/**", "**/*.pyc", "**/node_modules/**",
        "**/.git/**", "**/dist/**", "**/build/**", "**/.venv/**",
        "**/venv/**", "**/*.lock", "**/*.log", "**/contextpack_output/**",
        "**/.contextpack.yml", "**/*.min.js", "**/*.min.css",
        "**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif", "**/*.ico",
        "**/*.woff", "**/*.woff2", "**/*.ttf", "**/*.eot",
    ])
    max_file_size_kb: int = 500
    max_pages_per_file: int = 5
    summary_mode: str = "local"  # "api" | "local" | "none"
    api_key: Optional[str] = None
    language: str = "fr"
    output_formats: List[str] = field(default_factory=lambda: ["pdf", "markdown"])


DEFAULT_CONFIG_CONTENT = """\
# ContextPack Configuration
# Documentation: https://github.com/contextpack/contextpack

# Fichiers à inclure (glob patterns)
include:
  - "**/*.py"
  - "**/*.js"
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.go"
  - "**/*.rs"
  - "**/*.java"
  - "**/*.md"
  - "**/*.toml"
  - "**/*.yaml"
  - "**/*.yml"
  - "**/*.json"
  - "**/*.sh"
  - "**/*.env.example"

# Fichiers/dossiers à exclure
exclude:
  - "**/__pycache__/**"
  - "**/*.pyc"
  - "**/node_modules/**"
  - "**/.git/**"
  - "**/dist/**"
  - "**/build/**"
  - "**/.venv/**"
  - "**/venv/**"
  - "**/*.lock"
  - "**/*.log"
  - "**/contextpack_output/**"
  - "**/*.min.js"
  - "**/*.min.css"

# Taille max par fichier (en Ko)
max_file_size_kb: 500

# Nombre max de pages PDF par fichier
max_pages_per_file: 5

# Mode résumé IA: "api" | "local" | "none"
summary_mode: "local"

# Clé API Anthropic (optionnel, préférer variable d'env ANTHROPIC_API_KEY)
# api_key: "sk-ant-..."

# Langue du résumé
language: "fr"

# Formats de sortie
output_formats:
  - pdf
  - markdown
"""


def load_config(project_path: Path) -> Config:
    config_file = project_path / ".contextpack.yml"
    if not config_file.exists():
        return Config()

    with open(config_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return Config(
        include=data.get("include", Config().include),
        exclude=data.get("exclude", Config().exclude),
        max_file_size_kb=data.get("max_file_size_kb", 500),
        max_pages_per_file=data.get("max_pages_per_file", 5),
        summary_mode=data.get("summary_mode", "local"),
        api_key=data.get("api_key"),
        language=data.get("language", "fr"),
        output_formats=data.get("output_formats", ["pdf", "markdown"]),
    )


def create_default_config(config_file: Path):
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(DEFAULT_CONFIG_CONTENT)

```

---

## `contextpack\exporter.py`
*Taille: 13.1 Ko • ~3,342 tokens • python*

```python
"""Export Markdown consolidé et PDF paginé"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


# ──────────────────────────────────────────────
# MARKDOWN EXPORT
# ──────────────────────────────────────────────

def export_markdown(
    files: List[Dict[str, Any]],
    out_dir: Path,
    summary: str,
    project_path: Path,
) -> Path:
    """Génère un fichier Markdown consolidé avec tous les fichiers du projet."""
    project_name = project_path.resolve().name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"{project_name}_context_{timestamp}.md"

    lines = []

    # En-tête
    lines.append(f"# 📦 ContextPack — {project_name}")
    lines.append(f"\n> Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} par ContextPack")
    lines.append(f"> {len(files)} fichiers • {sum(f['size'] for f in files) / 1024:.1f} Ko total")
    lines.append("")

    # Résumé IA
    if summary:
        lines.append("---")
        lines.append("")
        lines.append(summary)
        lines.append("")
        lines.append("---")
        lines.append("")

    # Table des matières
    lines.append("## 📚 Table des matières\n")
    for i, f in enumerate(files, 1):
        anchor = f["rel_path"].replace("/", "").replace(".", "").replace("_", "").lower()
        lines.append(f"{i}. [{f['rel_path']}](#{anchor})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Fichiers
    for f in files:
        anchor = f["rel_path"].replace("/", "").replace(".", "").replace("_", "").lower()
        size_kb = f["size"] / 1024
        tokens = f.get("tokens", 0)

        lines.append(f"## `{f['rel_path']}`")
        lines.append(f"*Taille: {size_kb:.1f} Ko • ~{tokens:,} tokens • {f['language']}*")
        lines.append("")
        lines.append(f"```{f['language']}")
        lines.append(f["content"])
        if not f["content"].endswith("\n"):
            lines.append("")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Footer
    lines.append(f"\n*Pack généré par [ContextPack](https://github.com/contextpack/contextpack)*")

    content = "\n".join(lines)
    out_path.write_text(content, encoding="utf-8")
    return out_path


# ──────────────────────────────────────────────
# PDF EXPORT
# ──────────────────────────────────────────────

def export_pdf(
    files: List[Dict[str, Any]],
    out_dir: Path,
    summary: str,
    project_path: Path,
    max_pages_per_file: int = 5,
) -> Path:
    """Génère un PDF paginé et professionnel avec tous les fichiers du projet."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        HRFlowable, Preformatted, KeepTogether
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

    project_name = project_path.resolve().name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"{project_name}_context_{timestamp}.pdf"

    # ── Styles ──
    styles = getSampleStyleSheet()
    palette = {
        "bg_header": colors.HexColor("#1a1a2e"),
        "accent": colors.HexColor("#4361ee"),
        "accent2": colors.HexColor("#7209b7"),
        "code_bg": colors.HexColor("#f8f9fa"),
        "code_text": colors.HexColor("#212529"),
        "muted": colors.HexColor("#6c757d"),
        "white": colors.white,
        "hr": colors.HexColor("#dee2e6"),
    }

    style_title = ParagraphStyle(
        "CPTitle", parent=styles["Title"],
        fontSize=24, textColor=palette["white"],
        spaceAfter=6, fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    style_subtitle = ParagraphStyle(
        "CPSubtitle", parent=styles["Normal"],
        fontSize=10, textColor=colors.HexColor("#adb5bd"),
        spaceAfter=4, fontName="Helvetica",
        alignment=TA_CENTER,
    )
    style_h1 = ParagraphStyle(
        "CPH1", parent=styles["Heading1"],
        fontSize=14, textColor=palette["accent"],
        spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold",
        borderPad=4,
    )
    style_h2 = ParagraphStyle(
        "CPH2", parent=styles["Heading2"],
        fontSize=11, textColor=palette["bg_header"],
        spaceBefore=8, spaceAfter=4, fontName="Helvetica-Bold",
    )
    style_file_header = ParagraphStyle(
        "CPFileHeader", parent=styles["Normal"],
        fontSize=12, textColor=palette["white"],
        fontName="Helvetica-Bold", spaceAfter=2,
        backColor=palette["accent"], borderPad=6,
        leftIndent=4,
    )
    style_meta = ParagraphStyle(
        "CPMeta", parent=styles["Normal"],
        fontSize=8, textColor=palette["muted"],
        fontName="Helvetica", spaceAfter=4,
    )
    style_body = ParagraphStyle(
        "CPBody", parent=styles["Normal"],
        fontSize=9, textColor=colors.HexColor("#212529"),
        fontName="Helvetica", spaceAfter=4, leading=14,
    )
    style_code = ParagraphStyle(
        "CPCode", parent=styles["Code"],
        fontSize=7.5, fontName="Courier",
        textColor=palette["code_text"],
        backColor=palette["code_bg"],
        borderPad=6, spaceAfter=4, leading=11,
        leftIndent=6, rightIndent=6,
    )
    style_toc_item = ParagraphStyle(
        "CPTocItem", parent=styles["Normal"],
        fontSize=9, fontName="Helvetica",
        spaceAfter=2, leftIndent=12,
        textColor=colors.HexColor("#495057"),
    )
    style_summary = ParagraphStyle(
        "CPSummary", parent=styles["Normal"],
        fontSize=9, fontName="Helvetica",
        spaceAfter=6, leading=14,
        textColor=colors.HexColor("#212529"),
    )

    story = []
    PAGE_W, PAGE_H = A4

    # ── Page de couverture ──
    def cover_page():
        # Espace en haut
        story.append(Spacer(1, 3 * cm))
        story.append(Paragraph(f"🧠 ContextPack", style_title))
        story.append(Paragraph(project_name, ParagraphStyle(
            "CPProjectName", parent=style_title,
            fontSize=18, textColor=palette["accent"],
        )))
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph(
            f"Pack de contexte IA — {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            style_subtitle,
        ))
        total_size = sum(f["size"] for f in files)
        total_tokens = sum(f.get("tokens", 0) for f in files)
        story.append(Paragraph(
            f"{len(files)} fichiers • {total_size / 1024:.1f} Ko • ~{total_tokens:,} tokens estimés",
            style_subtitle,
        ))
        story.append(Spacer(1, 1 * cm))
        story.append(HRFlowable(width="80%", thickness=2, color=palette["accent"], spaceAfter=8))
        story.append(PageBreak())

    cover_page()

    # ── Table des matières ──
    story.append(Paragraph("📚 Table des matières", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=palette["hr"], spaceAfter=8))
    if summary:
        story.append(Paragraph("→ Résumé IA du projet", style_toc_item))
    for i, f in enumerate(files, 1):
        story.append(Paragraph(f"{i:02d}. {f['rel_path']}", style_toc_item))
    story.append(PageBreak())

    # ── Résumé IA ──
    if summary:
        story.append(Paragraph("🤖 Résumé IA du projet", style_h1))
        story.append(HRFlowable(width="100%", thickness=1, color=palette["hr"], spaceAfter=8))
        _render_markdown_summary(summary, story, style_summary, style_h1, style_h2, palette)
        story.append(PageBreak())

    # ── Fichiers ──
    for f in files:
        # Header fichier
        story.append(Paragraph(f"📄 {f['rel_path']}", style_file_header))
        size_kb = f["size"] / 1024
        tokens = f.get("tokens", 0)
        story.append(Paragraph(
            f"Taille: {size_kb:.1f} Ko  •  Tokens estimés: {tokens:,}  •  Langage: {f['language']}",
            style_meta,
        ))
        story.append(HRFlowable(width="100%", thickness=0.5, color=palette["hr"], spaceAfter=4))

        # Contenu (limité en pages)
        content = f["content"]
        lines = content.splitlines()

        # Estimation: ~60 lignes par page, max_pages_per_file pages
        max_lines = max_pages_per_file * 55
        truncated = False
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            truncated = True

        # Sécuriser le contenu pour ReportLab
        safe_content = _escape_for_reportlab("\n".join(lines))
        story.append(Preformatted(safe_content, style_code))

        if truncated:
            story.append(Paragraph(
                f"[... fichier tronqué — {len(content.splitlines()) - max_lines} lignes supplémentaires non affichées ...]",
                style_meta,
            ))

        story.append(Spacer(1, 0.3 * cm))
        story.append(HRFlowable(width="100%", thickness=1, color=palette["hr"], spaceAfter=4))
        story.append(PageBreak())

    # ── Build ──
    def on_page(canvas, doc):
        """Header et footer sur chaque page."""
        canvas.saveState()
        # Footer
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(palette["muted"])
        canvas.drawString(1.5 * cm, 0.8 * cm, f"ContextPack — {project_name}")
        canvas.drawRightString(PAGE_W - 1.5 * cm, 0.8 * cm, f"Page {doc.page}")
        # Ligne footer
        canvas.setStrokeColor(palette["hr"])
        canvas.setLineWidth(0.5)
        canvas.line(1.5 * cm, 1.2 * cm, PAGE_W - 1.5 * cm, 1.2 * cm)
        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title=f"ContextPack — {project_name}",
        author="ContextPack",
        subject="Pack de contexte IA",
    )
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return out_path


def _escape_for_reportlab(text: str) -> str:
    """Sécurise le texte pour l'affichage dans ReportLab (Preformatted)."""
    # Garder uniquement les caractères ASCII imprimables + quelques spéciaux
    result = []
    for char in text:
        code = ord(char)
        if char in ("\n", "\t"):
            result.append(char)
        elif 32 <= code <= 126:
            result.append(char)
        elif code > 127:
            # Garder les accents et caractères latin
            try:
                char.encode("latin-1")
                result.append(char)
            except (UnicodeEncodeError, UnicodeDecodeError):
                result.append("?")
        else:
            result.append(" ")
    return "".join(result)


def _render_markdown_summary(
    summary: str,
    story: list,
    style_body,
    style_h1,
    style_h2,
    palette: dict,
):
    """Convertit le Markdown du résumé en éléments ReportLab."""
    from reportlab.platypus import HRFlowable, Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib import colors

    style_h3 = ParagraphStyle(
        "CPH3", parent=style_body,
        fontSize=10, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#343a40"),
        spaceBefore=6, spaceAfter=3,
    )

    for line in summary.splitlines():
        stripped = line.strip()
        if not stripped:
            story.append(HRFlowable(width="100%", thickness=0, spaceAfter=3))
            continue
        if stripped.startswith("## "):
            story.append(HRFlowable(width="100%", thickness=0.5, color=palette["hr"], spaceAfter=4))
            story.append(Paragraph(_md_inline(stripped[3:]), style_h2))
        elif stripped.startswith("### "):
            story.append(Paragraph(_md_inline(stripped[4:]), style_h3))
        elif stripped.startswith("# "):
            pass  # Titre principal déjà dans le header
        elif stripped.startswith("- ") or stripped.startswith("* "):
            content = stripped[2:]
            story.append(Paragraph(f"• {_md_inline(content)}", ParagraphStyle(
                "CPBullet", parent=style_body,
                leftIndent=12, spaceAfter=2,
            )))
        elif stripped.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=1, color=palette["hr"], spaceAfter=6))
        else:
            story.append(Paragraph(_md_inline(stripped), style_body))


def _md_inline(text: str) -> str:
    """Convertit le Markdown inline basique en HTML ReportLab."""
    import re
    text = _escape_for_reportlab(text)
    # Bold **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Italic *text*
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    # Code `text`
    text = re.sub(r"`(.+?)`", r'<font name="Courier" size="8">\1</font>', text)
    return text

```

---

## `contextpack\scanner.py`
*Taille: 6.8 Ko • ~1,566 tokens • python*

```python
"""Scanner de fichiers du projet avec support .gitignore et estimation tokens"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import os
import fnmatch
import time

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import Config

console = Console()


def _matches_patterns(rel_path: str, patterns: List[str]) -> bool:
    """Vérifie si un chemin relatif correspond à l'un des patterns glob."""
    rel_posix = rel_path.replace("\\", "/")
    for pattern in patterns:
        pattern = pattern.replace("\\", "/")
        if fnmatch.fnmatch(rel_posix, pattern):
            return True
        # Match aussi le nom de fichier seul
        filename = rel_posix.split("/")[-1]
        if "/" not in pattern and fnmatch.fnmatch(filename, pattern):
            return True
        # Support des patterns comme **/foo/**
        if "**" in pattern:
            parts = pattern.split("**/")
            for part in parts:
                if part and fnmatch.fnmatch(rel_posix, f"*{part}*"):
                    return True
    return False


def _load_gitignore(project_path: Path) -> List[str]:
    """Charge les patterns .gitignore s'ils existent."""
    gitignore = project_path / ".gitignore"
    patterns = []
    if gitignore.exists():
        with open(gitignore, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(f"**/{line}/**")
                    patterns.append(f"**/{line}")
    return patterns


def _get_git_modified_files(project_path: Path) -> Optional[List[str]]:
    """Retourne la liste des fichiers modifiés depuis le dernier commit git."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")
    except Exception:
        pass
    return None


def _estimate_tokens(content: str) -> int:
    """Estimation rapide des tokens (~4 chars par token pour le code)."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(content))
    except Exception:
        return len(content) // 4


def _detect_language(path: Path) -> str:
    """Détecte le langage de programmation pour la coloration syntaxique."""
    ext_map = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".tsx": "tsx", ".jsx": "jsx", ".go": "go", ".rs": "rust",
        ".java": "java", ".c": "c", ".cpp": "cpp", ".cs": "csharp",
        ".rb": "ruby", ".php": "php", ".swift": "swift", ".kt": "kotlin",
        ".sh": "bash", ".bash": "bash", ".zsh": "bash",
        ".md": "markdown", ".yml": "yaml", ".yaml": "yaml",
        ".json": "json", ".toml": "toml", ".sql": "sql",
        ".html": "html", ".css": "css", ".scss": "scss",
        ".xml": "xml", ".env": "bash", ".txt": "text",
    }
    return ext_map.get(path.suffix.lower(), "text")


def scan_project(
    project_path: Path,
    config: Config,
    since_git: bool = False,
    estimate_tokens: bool = True,
) -> List[Dict[str, Any]]:
    """
    Scanne le projet et retourne la liste des fichiers avec leurs métadonnées.
    
    Returns: Liste de dicts avec keys:
        - path: Path absolu
        - rel_path: chemin relatif au projet
        - content: contenu du fichier
        - size: taille en octets
        - mtime: timestamp de modification
        - language: langage détecté
        - tokens: estimation tokens (si estimate_tokens=True)
    """
    git_ignore_patterns = _load_gitignore(project_path)
    all_exclude = config.exclude + git_ignore_patterns

    git_modified = None
    if since_git:
        git_modified = _get_git_modified_files(project_path)
        if git_modified is None:
            console.print("[yellow]⚠️  Git non disponible, scan complet.[/yellow]")

    files = []
    max_size = config.max_file_size_kb * 1024

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Scan en cours...", total=None)

        for root, dirs, filenames in os.walk(project_path):
            root_path = Path(root)
            rel_root = root_path.relative_to(project_path)

            # Exclure les dossiers cachés (sauf pour vérification explicite)
            dirs[:] = [
                d for d in dirs
                if not d.startswith(".")
                and not _matches_patterns(str(rel_root / d), all_exclude)
            ]

            for filename in filenames:
                file_path = root_path / filename
                rel_path = str(file_path.relative_to(project_path))

                # Filtre git --since
                if git_modified is not None:
                    if rel_path.replace("\\", "/") not in [m.replace("\\", "/") for m in git_modified]:
                        continue

                # Filtre include
                if not _matches_patterns(rel_path, config.include):
                    continue

                # Filtre exclude
                if _matches_patterns(rel_path, all_exclude):
                    continue

                # Taille
                try:
                    size = file_path.stat().st_size
                    mtime = file_path.stat().st_mtime
                except OSError:
                    continue

                if size > max_size:
                    console.print(f"[dim]⏭️  Ignoré (trop grand): {rel_path} ({size//1024}Ko)[/dim]")
                    continue

                # Lecture
                try:
                    content = file_path.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue

                if not content.strip():
                    continue

                token_count = _estimate_tokens(content) if estimate_tokens else 0

                files.append({
                    "path": file_path,
                    "rel_path": rel_path,
                    "content": content,
                    "size": size,
                    "mtime": mtime,
                    "language": _detect_language(file_path),
                    "tokens": token_count,
                })

                progress.update(task, description=f"Scan... {len(files)} fichiers trouvés")

    # Tri: fichiers principaux en premier, puis par chemin
    priority_names = {"README.md", "main.py", "index.ts", "index.js", "app.py", "main.go"}
    files.sort(key=lambda f: (
        0 if Path(f["rel_path"]).name in priority_names else 1,
        f["rel_path"]
    ))

    return files

```

---

## `contextpack\summarizer.py`
*Taille: 10.8 Ko • ~2,776 tokens • python*

```python
"""Génération de résumé IA — mode API Anthropic ou local (heuristique)"""

from typing import List, Dict, Any
from pathlib import Path


# ──────────────────────────────────────────────
# MODE API — Anthropic Claude
# ──────────────────────────────────────────────

def generate_summary(
    files: List[Dict[str, Any]],
    language: str = "fr",
    api_key: str = "",
    max_files_for_summary: int = 30,
) -> str:
    """
    Génère un résumé du projet via l'API Anthropic Claude.
    Envoie un échantillon des fichiers pour rester dans les limites de tokens.
    """
    import anthropic

    # Sélectionner les fichiers les plus importants (README + fichiers principaux)
    priority_exts = {".py", ".ts", ".js", ".go", ".rs", ".md", ".toml"}
    priority_files = [f for f in files if Path(f["rel_path"]).suffix in priority_exts]
    sample = priority_files[:max_files_for_summary] or files[:max_files_for_summary]

    # Construire le contexte à envoyer
    context_parts = []
    total_chars = 0
    char_limit = 60_000  # ~15k tokens

    for f in sample:
        snippet = f["content"][:3000]  # Max 3000 chars par fichier
        entry = f"### {f['rel_path']}\n```{f['language']}\n{snippet}\n```\n"
        if total_chars + len(entry) > char_limit:
            break
        context_parts.append(entry)
        total_chars += len(entry)

    file_list = "\n".join(f"- {f['rel_path']}" for f in files)
    context = "\n".join(context_parts)

    lang_instructions = {
        "fr": "Réponds en français.",
        "en": "Reply in English.",
        "es": "Responde en español.",
    }
    lang_instr = lang_instructions.get(language, f"Reply in {language}.")

    prompt = f"""Tu es un assistant technique expert. Analyse ce projet de code et génère un résumé structuré.

## Liste complète des fichiers du projet
{file_list}

## Extraits des fichiers principaux
{context}

## Ta mission
{lang_instr} Génère un résumé de reprise de contexte IA avec ces sections :

1. **Description du projet** — Que fait ce projet ? Quel est son objectif ?
2. **Architecture** — Structure des dossiers, technologies principales, patterns utilisés
3. **Fichiers clés** — Les 5-10 fichiers les plus importants et leur rôle
4. **État actuel** — Ce qui semble fonctionner, ce qui est en cours, les TODO visibles
5. **Points d'attention** — Dépendances importantes, configurations, variables d'environnement

Sois concis et précis. Ce résumé sera collé en début de nouvelle conversation IA pour reprendre le travail immédiatement."""

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


# ──────────────────────────────────────────────
# MODE LOCAL — Heuristique (sans API)
# ──────────────────────────────────────────────

def generate_summary_local(
    files: List[Dict[str, Any]],
    language: str = "fr",
) -> str:
    """
    Génère un résumé heuristique sans API :
    - Détecte le type de projet
    - Liste les fichiers clés
    - Extrait les imports, fonctions principales, TODO
    """
    from pathlib import Path
    from collections import Counter
    import re

    # ── Détection du type de projet ──
    ext_counts = Counter(Path(f["rel_path"]).suffix for f in files)
    all_names = [Path(f["rel_path"]).name for f in files]

    project_type = _detect_project_type(all_names, ext_counts)

    # ── Fichiers clés ──
    key_files = _find_key_files(files)

    # ── Extraction TODO/FIXME ──
    todos = _extract_todos(files)

    # ── Imports/dépendances ──
    deps = _extract_dependencies(files, all_names)

    # ── Construction du résumé ──
    lines = []

    if language == "fr":
        lines.append("# 🧠 Résumé de contexte — Généré par ContextPack\n")
        lines.append(f"## 📋 Type de projet détecté\n{project_type}\n")
        lines.append(f"## 📊 Vue d'ensemble\n- **{len(files)} fichiers** inclus dans ce pack")
        total_tokens = sum(f.get("tokens", 0) for f in files)
        lines.append(f"- **~{total_tokens:,} tokens** estimés au total\n")

        lines.append("## 📁 Fichiers clés")
        for rel, desc in key_files:
            lines.append(f"- `{rel}` — {desc}")
        lines.append("")

        if deps:
            lines.append("## 📦 Dépendances / Technologies détectées")
            for d in deps[:15]:
                lines.append(f"- {d}")
            lines.append("")

        if todos:
            lines.append("## 📝 TODO / FIXME détectés")
            for t in todos[:10]:
                lines.append(f"- {t}")
            lines.append("")

        lines.append("## 📂 Arborescence complète")
        lines.append("```")
        tree = _build_tree(files)
        lines.append(tree)
        lines.append("```\n")

        lines.append("---")
        lines.append("*Résumé généré en mode local (sans API). Pour un résumé IA complet, utilise `--summary api`.*")

    else:  # english fallback
        lines.append("# 🧠 Context Summary — Generated by ContextPack\n")
        lines.append(f"## 📋 Detected Project Type\n{project_type}\n")
        lines.append(f"## 📊 Overview\n- **{len(files)} files** included in this pack")
        total_tokens = sum(f.get("tokens", 0) for f in files)
        lines.append(f"- **~{total_tokens:,} tokens** estimated total\n")
        lines.append("## 📁 Key Files")
        for rel, desc in key_files:
            lines.append(f"- `{rel}` — {desc}")
        lines.append("")
        if deps:
            lines.append("## 📦 Dependencies / Technologies")
            for d in deps[:15]:
                lines.append(f"- {d}")
            lines.append("")
        if todos:
            lines.append("## 📝 TODO / FIXME")
            for t in todos[:10]:
                lines.append(f"- {t}")
            lines.append("")
        lines.append("## 📂 File Tree")
        lines.append("```")
        lines.append(_build_tree(files))
        lines.append("```\n")

    return "\n".join(lines)


def _detect_project_type(names: List[str], ext_counts) -> str:
    if "package.json" in names and ("next.config.js" in names or "next.config.ts" in names):
        return "Application **Next.js** (React + TypeScript)"
    if "package.json" in names and ext_counts.get(".tsx", 0) > 0:
        return "Application **React** (TypeScript)"
    if "package.json" in names and ext_counts.get(".ts", 0) > 0:
        return "Projet **Node.js / TypeScript**"
    if "package.json" in names:
        return "Projet **Node.js / JavaScript**"
    if "pyproject.toml" in names or "setup.py" in names or "setup.cfg" in names:
        return "Projet **Python** (package)"
    if ext_counts.get(".py", 0) > 3:
        if "manage.py" in names:
            return "Application **Django** (Python)"
        if "app.py" in names or "main.py" in names:
            return "Application **Python** (Flask / FastAPI / CLI)"
        return "Projet **Python**"
    if "go.mod" in names:
        return "Projet **Go**"
    if "Cargo.toml" in names:
        return "Projet **Rust**"
    if "pom.xml" in names or "build.gradle" in names:
        return "Projet **Java**"
    return "Projet de code (type non détecté automatiquement)"


def _find_key_files(files: List[Dict]) -> List[tuple]:
    key_map = {
        "README.md": "Documentation principale",
        "main.py": "Point d'entrée principal",
        "app.py": "Application principale",
        "index.ts": "Point d'entrée TypeScript",
        "index.js": "Point d'entrée JavaScript",
        "main.go": "Point d'entrée Go",
        "Cargo.toml": "Configuration Rust",
        "pyproject.toml": "Configuration Python",
        "package.json": "Dépendances Node.js",
        "go.mod": "Module Go",
        "docker-compose.yml": "Orchestration Docker",
        "Dockerfile": "Image Docker",
        ".env.example": "Variables d'environnement exemple",
        "requirements.txt": "Dépendances Python",
    }
    result = []
    file_names = {Path(f["rel_path"]).name: f["rel_path"] for f in files}
    for name, desc in key_map.items():
        if name in file_names:
            result.append((file_names[name], desc))
    return result[:10]


def _extract_todos(files: List[Dict]) -> List[str]:
    import re
    todos = []
    pattern = re.compile(r"(?:#|//|/\*)\s*(TODO|FIXME|HACK|NOTE|XXX):?\s*(.+)", re.IGNORECASE)
    for f in files:
        for line in f["content"].splitlines():
            m = pattern.search(line)
            if m:
                tag, msg = m.group(1).upper(), m.group(2).strip()
                todos.append(f"[{tag}] {msg[:80]} — `{f['rel_path']}`")
    return todos[:20]


def _extract_dependencies(files: List[Dict], names: List[str]) -> List[str]:
    deps = []
    import json, re
    for f in files:
        name = Path(f["rel_path"]).name
        if name == "package.json":
            try:
                data = json.loads(f["content"])
                for k in list(data.get("dependencies", {}).keys())[:10]:
                    deps.append(f"`{k}` (npm)")
            except Exception:
                pass
        elif name == "requirements.txt":
            for line in f["content"].splitlines():
                line = line.strip().split("==")[0].split(">=")[0]
                if line and not line.startswith("#"):
                    deps.append(f"`{line}` (pip)")
        elif name == "pyproject.toml":
            for line in f["content"].splitlines():
                m = re.search(r'"([a-zA-Z0-9_-]+)"\s*=', line)
                if m and "dependencies" in f["content"]:
                    deps.append(f"`{m.group(1)}` (pip)")
        elif name == "go.mod":
            for line in f["content"].splitlines():
                if line.startswith("\t") and "/" in line:
                    dep = line.strip().split()[0]
                    deps.append(f"`{dep}` (go)")
    return list(dict.fromkeys(deps))  # déduplique


def _build_tree(files: List[Dict]) -> str:
    from pathlib import PurePosixPath
    paths = sorted(f["rel_path"].replace("\\", "/") for f in files)
    lines = []
    seen_dirs = set()
    for p in paths:
        parts = p.split("/")
        for i in range(len(parts) - 1):
            d = "/".join(parts[:i+1])
            if d not in seen_dirs:
                lines.append("  " * i + f"📁 {parts[i]}/")
                seen_dirs.add(d)
        indent = "  " * (len(parts) - 1)
        lines.append(f"{indent}📄 {parts[-1]}")
    return "\n".join(lines[:80])  # Limite l'arbre

```

---

## `pyproject.toml`
*Taille: 0.9 Ko • ~272 tokens • toml*

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "contextpack"
version = "1.0.0"
description = "CLI de sauvegarde de contexte IA — Reprends n'importe quel projet après expiration du contexte"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
keywords = ["ai", "context", "llm", "cli", "pdf", "markdown"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Environment :: Console",
    "Topic :: Utilities",
]
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "reportlab>=4.0.0",
    "pathspec>=0.11.0",
    "tiktoken>=0.5.0",
    "anthropic>=0.25.0",
    "pyyaml>=6.0",
]

[project.scripts]
contextpack = "contextpack.cli:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["contextpack*"]

```

---


*Pack généré par [ContextPack](https://github.com/contextpack/contextpack)*