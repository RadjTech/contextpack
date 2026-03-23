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
