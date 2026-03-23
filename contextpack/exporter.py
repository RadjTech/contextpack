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
