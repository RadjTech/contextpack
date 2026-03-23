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
