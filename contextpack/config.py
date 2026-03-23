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
    max_pages_per_pack: Optional[int] = None   # None = un seul PDF sans limite
    summary_mode: str = "local"                 # "api" | "local" | "none"
    api_key: Optional[str] = None
    language: str = "fr"
    output_formats: List[str] = field(default_factory=lambda: ["pdf", "markdown"])


# ──────────────────────────────────────────────
# TEMPLATES PAR TYPE DE PROJET
# ──────────────────────────────────────────────

PROJECT_TEMPLATES = {
    "python": {
        "label": "Python (package / script)",
        "include": [
            "**/*.py", "**/*.md", "**/*.toml", "**/*.cfg", "**/*.ini",
            "**/*.yml", "**/*.yaml", "**/*.txt", "**/*.env.example", "**/*.sh",
        ],
        "exclude": [
            "**/__pycache__/**", "**/*.pyc", "**/*.pyo",
            "**/.venv/**", "**/venv/**", "**/env/**",
            "**/dist/**", "**/build/**", "**/*.egg-info/**",
            "**/.git/**", "**/*.lock", "**/*.log",
            "**/contextpack_output/**",
        ],
        "notes": "Python package / application",
    },
    "django": {
        "label": "Django",
        "include": [
            "**/*.py", "**/*.html", "**/*.md", "**/*.toml", "**/*.cfg",
            "**/*.yml", "**/*.yaml", "**/*.txt", "**/*.env.example",
            "**/templates/**/*.html", "**/static/**/*.css", "**/static/**/*.js",
        ],
        "exclude": [
            "**/__pycache__/**", "**/*.pyc", "**/.venv/**", "**/venv/**",
            "**/dist/**", "**/build/**", "**/*.egg-info/**",
            "**/migrations/0*.py",   # garde __init__ mais pas les migrations auto
            "**/.git/**", "**/*.lock", "**/*.log", "**/contextpack_output/**",
            "**/staticfiles/**", "**/media/**",
        ],
        "notes": "Django web application",
    },
    "fastapi": {
        "label": "FastAPI / Flask",
        "include": [
            "**/*.py", "**/*.md", "**/*.toml", "**/*.cfg",
            "**/*.yml", "**/*.yaml", "**/*.txt", "**/*.env.example",
            "**/*.json",
        ],
        "exclude": [
            "**/__pycache__/**", "**/*.pyc", "**/.venv/**", "**/venv/**",
            "**/dist/**", "**/build/**", "**/*.egg-info/**",
            "**/.git/**", "**/*.lock", "**/*.log", "**/contextpack_output/**",
        ],
        "notes": "FastAPI / Flask REST API",
    },
    "react_vite": {
        "label": "React + Vite (TypeScript)",
        "include": [
            "**/*.tsx", "**/*.ts", "**/*.jsx", "**/*.js",
            "**/*.css", "**/*.scss", "**/*.md",
            "**/*.json", "**/*.toml", "**/*.env.example",
            "vite.config.*", "tailwind.config.*", "tsconfig*.json",
        ],
        "exclude": [
            "**/node_modules/**", "**/dist/**", "**/build/**",
            "**/.git/**", "**/*.lock", "**/*.log",
            "**/contextpack_output/**", "**/*.min.js", "**/*.min.css",
            "**/coverage/**", "**/.cache/**",
            "**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif", "**/*.svg",
            "**/*.woff*", "**/*.ttf", "**/*.eot",
        ],
        "notes": "React + Vite application",
    },
    "nextjs": {
        "label": "Next.js",
        "include": [
            "**/*.tsx", "**/*.ts", "**/*.jsx", "**/*.js",
            "**/*.css", "**/*.scss", "**/*.md",
            "**/*.json", "**/*.env.example",
            "next.config.*", "tailwind.config.*", "tsconfig*.json",
        ],
        "exclude": [
            "**/node_modules/**", "**/.next/**", "**/out/**",
            "**/dist/**", "**/.git/**", "**/*.lock", "**/*.log",
            "**/contextpack_output/**", "**/*.min.js", "**/*.min.css",
            "**/coverage/**",
            "**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif",
            "**/*.woff*", "**/*.ttf",
        ],
        "notes": "Next.js application",
    },
    "flutter": {
        "label": "Flutter / Dart",
        "include": [
            "**/*.dart", "**/*.yaml", "**/*.yml", "**/*.md",
            "**/*.json", "**/*.env.example",
            "pubspec.yaml", "pubspec.lock",
            "android/app/build.gradle", "ios/Runner/Info.plist",
        ],
        "exclude": [
            "**/.dart_tool/**", "**/build/**", "**/.flutter-plugins*",
            "**/ios/Pods/**", "**/android/.gradle/**",
            "**/.git/**", "**/*.log", "**/contextpack_output/**",
            "**/.packages", "**/*.g.dart", "**/*.freezed.dart",
        ],
        "notes": "Flutter mobile/desktop application",
    },
    "go": {
        "label": "Go",
        "include": [
            "**/*.go", "**/*.mod", "**/*.sum", "**/*.md",
            "**/*.yaml", "**/*.yml", "**/*.toml",
            "**/*.env.example", "**/*.sh", "Dockerfile*",
        ],
        "exclude": [
            "**/vendor/**", "**/bin/**", "**/dist/**",
            "**/.git/**", "**/*.log", "**/contextpack_output/**",
        ],
        "notes": "Go application / service",
    },
    "rust": {
        "label": "Rust",
        "include": [
            "**/*.rs", "Cargo.toml", "Cargo.lock", "**/*.md",
            "**/*.yaml", "**/*.yml", "**/*.toml",
            "**/*.env.example", "**/*.sh",
        ],
        "exclude": [
            "**/target/**", "**/.git/**", "**/*.log",
            "**/contextpack_output/**",
        ],
        "notes": "Rust application / library",
    },
    "node": {
        "label": "Node.js / JavaScript",
        "include": [
            "**/*.js", "**/*.mjs", "**/*.cjs", "**/*.json",
            "**/*.md", "**/*.env.example", "**/*.sh",
            "**/*.yaml", "**/*.yml",
        ],
        "exclude": [
            "**/node_modules/**", "**/dist/**", "**/build/**",
            "**/.git/**", "**/*.lock", "**/*.log",
            "**/contextpack_output/**", "**/*.min.js",
        ],
        "notes": "Node.js application",
    },
    "java": {
        "label": "Java / Kotlin",
        "include": [
            "**/*.java", "**/*.kt", "**/*.xml", "**/*.gradle",
            "**/*.properties", "**/*.md", "**/*.yaml", "**/*.yml",
            "**/*.env.example",
        ],
        "exclude": [
            "**/target/**", "**/build/**", "**/.git/**",
            "**/bin/**", "**/*.class", "**/*.jar",
            "**/*.log", "**/contextpack_output/**",
        ],
        "notes": "Java / Kotlin / Spring project",
    },
    "generic": {
        "label": "Projet générique",
        "include": [
            "**/*.py", "**/*.js", "**/*.ts", "**/*.tsx", "**/*.jsx",
            "**/*.go", "**/*.rs", "**/*.java", "**/*.dart",
            "**/*.c", "**/*.cpp", "**/*.h",
            "**/*.md", "**/*.txt", "**/*.toml", "**/*.yaml", "**/*.yml",
            "**/*.json", "**/*.env.example", "**/*.sh",
        ],
        "exclude": [
            "**/__pycache__/**", "**/*.pyc", "**/node_modules/**",
            "**/.git/**", "**/dist/**", "**/build/**", "**/.venv/**",
            "**/venv/**", "**/*.lock", "**/*.log", "**/contextpack_output/**",
            "**/*.min.js", "**/*.min.css",
            "**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif", "**/*.ico",
            "**/*.woff*", "**/*.ttf", "**/*.eot",
        ],
        "notes": "Generic project",
    },
}


def detect_project_type(project_path: Path) -> str:
    """
    Détecte automatiquement le type de projet en inspectant les fichiers racine.
    Retourne la clé du template le plus adapté.
    """
    root_files = {f.name for f in project_path.iterdir() if f.is_file()}
    root_dirs = {d.name for d in project_path.iterdir() if d.is_dir()}

    # Flutter
    if "pubspec.yaml" in root_files and "lib" in root_dirs:
        return "flutter"

    # Next.js (avant React générique)
    if "package.json" in root_files:
        pkg_path = project_path / "package.json"
        try:
            import json
            pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps:
                return "nextjs"
            if "vite" in deps:
                return "react_vite"
        except Exception:
            pass
        # Fallback JS/TS
        return "node"

    # Python — détection fine
    if "pyproject.toml" in root_files or "setup.py" in root_files or "setup.cfg" in root_files:
        if "manage.py" in root_files:
            return "django"
        # Lire pyproject pour détecter fastapi/flask
        if "pyproject.toml" in root_files:
            try:
                content = (project_path / "pyproject.toml").read_text(encoding="utf-8").lower()
                if "fastapi" in content or "flask" in content or "starlette" in content:
                    return "fastapi"
            except Exception:
                pass
        return "python"

    if "requirements.txt" in root_files:
        try:
            content = (project_path / "requirements.txt").read_text(encoding="utf-8").lower()
            if "django" in content:
                return "django"
            if "fastapi" in content or "flask" in content:
                return "fastapi"
        except Exception:
            pass
        return "python"

    # Go
    if "go.mod" in root_files:
        return "go"

    # Rust
    if "Cargo.toml" in root_files:
        return "rust"

    # Java / Kotlin
    if "pom.xml" in root_files or "build.gradle" in root_files or "build.gradle.kts" in root_files:
        return "java"

    return "generic"


def _build_config_content(project_type: str, max_pages_per_pack: Optional[int] = None) -> str:
    tpl = PROJECT_TEMPLATES.get(project_type, PROJECT_TEMPLATES["generic"])

    include_lines = "\n".join(f'  - "{p}"' for p in tpl["include"])
    exclude_lines = "\n".join(f'  - "{p}"' for p in tpl["exclude"])

    max_pages_line = (
        f"max_pages_per_pack: {max_pages_per_pack}"
        if max_pages_per_pack
        else "# max_pages_per_pack: 50  # décommente pour splitter en volumes PDF"
    )

    return f"""\
# ContextPack Configuration — {tpl['label']}
# Documentation: https://github.com/contextpack/contextpack

# Fichiers à inclure (glob patterns)
include:
{include_lines}

# Fichiers/dossiers à exclure
exclude:
{exclude_lines}

# Taille max par fichier (en Ko)
max_file_size_kb: 500

# Nombre max de pages par volume PDF (None = un seul PDF)
# Si défini, le pack crée PDF-part1, PDF-part2, etc.
{max_pages_line}

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
        max_pages_per_pack=data.get("max_pages_per_pack", None),
        summary_mode=data.get("summary_mode", "local"),
        api_key=data.get("api_key"),
        language=data.get("language", "fr"),
        output_formats=data.get("output_formats", ["pdf", "markdown"]),
    )


def create_default_config(config_file: Path, project_type: str = "generic"):
    content = _build_config_content(project_type)
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(content)