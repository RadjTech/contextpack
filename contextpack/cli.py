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
from rich.table import Table
from rich import box

from .scanner import scan_project
from .exporter import export_markdown, export_pdf
from .summarizer import generate_summary, generate_summary_local
from .config import (
    load_config, create_default_config, Config,
    detect_project_type, PROJECT_TEMPLATES,
)

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


def _resolve_path(path: Path) -> Path:
    """Résout et valide le chemin du projet."""
    resolved = path.resolve()
    if not resolved.exists():
        console.print(f"[red]❌ Dossier introuvable : {resolved}[/red]")
        raise typer.Exit(1)
    if not resolved.is_dir():
        console.print(f"[red]❌ Ce chemin n'est pas un dossier : {resolved}[/red]")
        raise typer.Exit(1)
    return resolved


@app.command("init")
def cmd_init(
    path: Path = typer.Argument(Path("."), help="Répertoire du projet (chemin absolu ou relatif)"),
    project_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help="Type de projet : python, django, fastapi, react_vite, nextjs, flutter, go, rust, node, java, generic",
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Écraser sans confirmation"),
):
    """
    ⚙️  Initialise un .contextpack.yml adapté au type de projet.

    Exemples:\n
        contextpack init\n
        contextpack init ~/mes-projets/mon-app\n
        contextpack init --type flutter\n
        contextpack init /chemin/absolu/vers/projet --type nextjs
    """
    print_banner()
    resolved = _resolve_path(path)
    config_file = resolved / ".contextpack.yml"

    if config_file.exists() and not force:
        overwrite = typer.confirm("⚠️  .contextpack.yml existe déjà. Écraser ?")
        if not overwrite:
            raise typer.Exit()

    # Détection automatique si pas de --type
    if project_type is None:
        detected = detect_project_type(resolved)
        tpl_label = PROJECT_TEMPLATES[detected]["label"]
        console.print(f"[cyan]🔍 Projet détecté :[/cyan] [bold]{tpl_label}[/bold]")
        project_type = detected
    else:
        if project_type not in PROJECT_TEMPLATES:
            valid = ", ".join(PROJECT_TEMPLATES.keys())
            console.print(f"[red]❌ Type inconnu : '{project_type}'. Valeurs valides : {valid}[/red]")
            raise typer.Exit(1)
        console.print(f"[cyan]📋 Template :[/cyan] [bold]{PROJECT_TEMPLATES[project_type]['label']}[/bold]")

    create_default_config(config_file, project_type)
    console.print(f"[green]✅ Config créée :[/green] {config_file}")
    console.print("[dim]Édite .contextpack.yml pour personnaliser les fichiers inclus/exclus.[/dim]")

    # Afficher un résumé des patterns
    from .config import PROJECT_TEMPLATES as TPLS
    tpl = TPLS[project_type]
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan")
    table.add_column("Include", style="green")
    table.add_column("Exclude", style="red")
    inc = tpl["include"]
    exc = tpl["exclude"]
    for i in range(max(len(inc), len(exc))):
        table.add_row(
            inc[i] if i < len(inc) else "",
            exc[i] if i < len(exc) else "",
        )
    console.print(table)


@app.command("init-list")
def cmd_init_list():
    """📋 Liste tous les types de projets disponibles pour --type."""
    print_banner()
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan", title="Types de projets disponibles")
    table.add_column("Clé (--type)", style="bold yellow")
    table.add_column("Label", style="white")
    for key, tpl in PROJECT_TEMPLATES.items():
        table.add_row(key, tpl["label"])
    console.print(table)


@app.command("pack")
def cmd_pack(
    path: Path = typer.Argument(Path("."), help="Répertoire du projet (chemin absolu ou relatif)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Dossier de sortie (défaut: <projet>/contextpack_output)"),
    pdf: bool = typer.Option(True, "--pdf/--no-pdf", help="Générer le PDF"),
    markdown: bool = typer.Option(True, "--markdown/--no-markdown", help="Générer le Markdown"),
    summary: Optional[str] = typer.Option(None, "--summary", "-s", help="Mode résumé IA : 'api' | 'local' | 'none'"),
    api_key: Optional[str] = typer.Option(None, "--api-key", envvar="ANTHROPIC_API_KEY", help="Clé API Anthropic"),
    max_pages: Optional[int] = typer.Option(
        None, "--max-pages", "-p",
        help="Nombre max de pages par volume PDF. Si défini, crée PDF-part1, PDF-part2... (défaut: un seul PDF sans limite)",
    ),
    since_git: bool = typer.Option(False, "--since-git", help="Inclure seulement les fichiers modifiés depuis le dernier commit"),
    language: str = typer.Option("fr", "--lang", "-l", help="Langue du résumé (fr, en, ...)"),
    estimate_tokens: bool = typer.Option(True, "--tokens/--no-tokens", help="Estimer les tokens"),
):
    """
    📦 Génère un pack de contexte complet du projet.

    Exemples:\n
        contextpack pack\n
        contextpack pack ~/mes-projets/mon-app\n
        contextpack pack /chemin/absolu --summary api\n
        contextpack pack --max-pages 50 -o ~/Desktop/pack\n
        contextpack pack --since-git --lang en
    """
    print_banner()

    resolved = _resolve_path(path)
    console.print(f"[dim]📂 Projet : {resolved}[/dim]")

    config = load_config(resolved)

    # max_pages CLI > config YAML
    effective_max_pages = max_pages if max_pages is not None else config.max_pages_per_pack

    out_dir = output or (resolved / "contextpack_output")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Scanner
    console.print("\n[bold cyan]📁 Scan du projet...[/bold cyan]")
    files = scan_project(resolved, config, since_git=since_git, estimate_tokens=estimate_tokens)

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
            else:
                summary_text = generate_summary_local(files, language)
            console.print("[green]✅ Résumé généré[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Erreur résumé: {e}. Passage sans résumé.[/yellow]")

    # Export Markdown
    md_path = None
    if markdown:
        console.print("\n[bold cyan]📝 Export Markdown...[/bold cyan]")
        md_path = export_markdown(files, out_dir, summary_text, resolved)
        console.print(f"[green]✅ Markdown :[/green] {md_path}")

    # Export PDF
    pdf_paths = []
    if pdf:
        if effective_max_pages:
            console.print(f"\n[bold cyan]📄 Export PDF (volumes de {effective_max_pages} pages max)...[/bold cyan]")
        else:
            console.print("\n[bold cyan]📄 Export PDF (document complet)...[/bold cyan]")

        pdf_paths = export_pdf(files, out_dir, summary_text, resolved, max_pages_per_pack=effective_max_pages)

        if len(pdf_paths) == 1:
            console.print(f"[green]✅ PDF :[/green] {pdf_paths[0]}")
        else:
            console.print(f"[green]✅ {len(pdf_paths)} volumes PDF générés :[/green]")
            for p in pdf_paths:
                console.print(f"   [cyan]•[/cyan] {p.name}")

    # Résumé final
    total_size   = sum(f["size"] for f in files)
    total_tokens = sum(f.get("tokens", 0) for f in files)

    pdf_info = (
        f"[cyan]{len(pdf_paths)} volume(s)[/cyan]"
        if pdf_paths else "[dim]non généré[/dim]"
    )

    console.print(Panel(
        f"[bold green]Pack généré avec succès ![/bold green]\n\n"
        f"  📂 Fichiers    : [cyan]{len(files)}[/cyan]\n"
        f"  📦 Taille      : [cyan]{total_size / 1024:.1f} Ko[/cyan]\n"
        f"  🔢 Tokens est. : [cyan]{total_tokens:,}[/cyan]\n"
        f"  📄 PDF         : {pdf_info}\n"
        f"  📁 Sortie      : [cyan]{out_dir}[/cyan]",
        border_style="green",
        title="✅ Résultat",
    ))

    project_name = resolved.name
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
    path: Path = typer.Argument(Path("."), help="Répertoire du projet (chemin absolu ou relatif)"),
):
    """🔍 Affiche les fichiers modifiés depuis le dernier pack."""
    print_banner()
    from datetime import datetime

    resolved = _resolve_path(path)
    out_dir = resolved / "contextpack_output"
    last_pack = None

    if out_dir.exists():
        packs = sorted(out_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        if packs:
            last_pack = packs[0]

    if not last_pack:
        console.print("[yellow]Aucun pack précédent trouvé. Lance 'contextpack pack' d'abord.[/yellow]")
        raise typer.Exit()

    pack_time = last_pack.stat().st_mtime
    pack_dt   = datetime.fromtimestamp(pack_time)
    console.print(f"[dim]Dernier pack : {pack_dt.strftime('%d/%m/%Y %H:%M')}[/dim]\n")

    config = load_config(resolved)
    files  = scan_project(resolved, config)

    changed   = [f for f in files if f["mtime"] > pack_time]
    unchanged = [f for f in files if f["mtime"] <= pack_time]

    if changed:
        console.print(f"[bold yellow]📝 {len(changed)} fichier(s) modifié(s) depuis le dernier pack :[/bold yellow]")
        for f in changed:
            console.print(f"  [yellow]~[/yellow] {f['rel_path']}")
    else:
        console.print("[green]✅ Aucun fichier modifié depuis le dernier pack.[/green]")

    console.print(f"\n[dim]{len(unchanged)} fichiers inchangés[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()