# 🧠 ContextPack

> **Reprends n'importe quel projet IA en 30 secondes après expiration du contexte.**

Quand le contexte d'une conversation IA expire, tu perds tout le fil. ContextPack génère automatiquement un **pack de reprise** — un PDF ou Markdown consolidé avec tous tes fichiers + un résumé IA — prêt à coller dans une nouvelle conversation.

---

## ✨ Fonctionnalités

- 📁 **Scan intelligent** — Détecte automatiquement les fichiers pertinents, respecte `.gitignore`
- 🤖 **Résumé IA** — Via API Anthropic Claude ou génération locale (sans API)
- 📄 **Export PDF multi-volumes** — Pack illimité en pages, ou splitté en volumes (`--max-pages 50`)
- 📝 **Export Markdown** — Fichier unique consolidé, parfait à coller dans une conversation
- 🔢 **Estimation tokens** — Sais exactement combien de tokens ton pack va consommer
- 🔍 **Mode diff** — Vois quels fichiers ont changé depuis le dernier pack
- ⚙️  **Init intelligent** — Détecte ton type de projet et génère un `.contextpack.yml` adapté
- 📂 **Chemin direct** — Passe n'importe quel dossier en argument, absolu ou relatif

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
# Pack du dossier courant
contextpack pack

# Pack d'un dossier spécifique (chemin relatif ou absolu)
contextpack pack ~/mes-projets/mon-app
contextpack pack /chemin/absolu/vers/projet
contextpack pack ../autre-projet

# Avec résumé IA via API
contextpack pack --summary api --api-key sk-ant-...
export ANTHROPIC_API_KEY=sk-ant-...
contextpack pack ~/mon-projet --summary api

# PDF splitté en volumes de 50 pages max (→ part1.pdf, part2.pdf…)
contextpack pack --max-pages 50

# PDF complet sans limite (défaut)
contextpack pack --no-max-pages   # ou simplement ne pas passer --max-pages

# Dossier de sortie personnalisé
contextpack pack ~/mon-projet -o ~/Desktop/mon_pack

# Seulement les fichiers modifiés depuis le dernier commit git
contextpack pack --since-git

# Résumé en anglais
contextpack pack --lang en
```

### Initialiser la config (détection automatique du type de projet)

```bash
# Détection automatique dans le dossier courant
contextpack init

# Initialiser un dossier spécifique
contextpack init ~/mes-projets/mon-app
contextpack init /chemin/absolu/vers/projet

# Forcer un type de projet
contextpack init --type flutter
contextpack init ~/mon-app --type nextjs
contextpack init --type django

# Voir tous les types disponibles
contextpack init-list
```

**Types supportés :** `python`, `django`, `fastapi`, `react_vite`, `nextjs`, `flutter`, `go`, `rust`, `node`, `java`, `generic`

### Voir les fichiers modifiés

```bash
contextpack diff
contextpack diff ~/mon-projet
```

---

## ⚙️ Configuration `.contextpack.yml`

```yaml
# Fichiers à inclure
include:
  - "**/*.py"
  - "**/*.md"
  - "**/*.toml"

# Fichiers à exclure
exclude:
  - "**/__pycache__/**"
  - "**/dist/**"

# Taille max par fichier (Ko)
max_file_size_kb: 500

# Nombre max de pages par volume PDF
# Si défini → crée plusieurs PDFs (part1, part2…)
# Si absent → un seul PDF complet sans limite de pages
# max_pages_per_pack: 50

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

## 📄 PDF multi-volumes

Par défaut, ContextPack génère **un seul PDF complet** sans limite de pages — idéal pour les gros projets.

Si tu veux splitter en volumes (ex : pour l'upload dans une interface qui limite la taille des fichiers) :

```bash
# Via CLI
contextpack pack --max-pages 50

# Via .contextpack.yml
max_pages_per_pack: 50
```

Cela génère :
```
projet_context_20240101_120000_part1.pdf   (≤ 50 pages)
projet_context_20240101_120000_part2.pdf   (≤ 50 pages)
...
```

Le résumé IA apparaît uniquement dans le **volume 1**. Chaque volume a sa propre couverture et table des matières.

---

## 🔑 Modes de résumé IA

| Mode | Description | Qualité | Coût |
|------|-------------|---------|------|
| `api` | Claude analyse ton code via l'API Anthropic | ⭐⭐⭐⭐⭐ | Quelques centimes |
| `local` | Heuristique locale (sans API) | ⭐⭐⭐ | Gratuit |
| `none` | Pas de résumé, juste les fichiers | — | Gratuit |

---

## 🧩 Templates de config par type de projet

`contextpack init` détecte automatiquement ton type de projet en inspectant les fichiers racine :

| Fichier détecté | Type de projet |
|----------------|----------------|
| `pubspec.yaml` + `lib/` | Flutter |
| `package.json` + `next` dep | Next.js |
| `package.json` + `vite` dep | React + Vite |
| `package.json` | Node.js |
| `pyproject.toml` + `manage.py` | Django |
| `pyproject.toml` / `setup.py` | Python |
| `requirements.txt` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml` / `build.gradle` | Java / Kotlin |

---

## 💬 Prompt de reprise suggéré

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
