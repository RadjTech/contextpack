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
