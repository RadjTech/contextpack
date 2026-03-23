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
