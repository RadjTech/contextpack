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
