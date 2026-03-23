"""Export Markdown consolidé et PDF paginé (multi-volumes si max_pages_per_pack défini)"""

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

    lines.append(f"# 📦 ContextPack — {project_name}")
    lines.append(f"\n> Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} par ContextPack")
    lines.append(f"> {len(files)} fichiers • {sum(f['size'] for f in files) / 1024:.1f} Ko total")
    lines.append("")

    if summary:
        lines.append("---")
        lines.append("")
        lines.append(summary)
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## 📚 Table des matières\n")
    for i, f in enumerate(files, 1):
        anchor = f["rel_path"].replace("/", "").replace(".", "").replace("_", "").lower()
        lines.append(f"{i}. [{f['rel_path']}](#{anchor})")
    lines.append("")
    lines.append("---")
    lines.append("")

    for f in files:
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

    lines.append(f"\n*Pack généré par [ContextPack](https://github.com/contextpack/contextpack)*")

    content = "\n".join(lines)
    out_path.write_text(content, encoding="utf-8")
    return out_path


# ──────────────────────────────────────────────
# PDF EXPORT — multi-volumes
# ──────────────────────────────────────────────

def export_pdf(
    files: List[Dict[str, Any]],
    out_dir: Path,
    summary: str,
    project_path: Path,
    max_pages_per_pack: Optional[int] = None,
) -> List[Path]:
    """
    Génère un ou plusieurs PDFs du projet.

    - Si max_pages_per_pack est None → un seul PDF complet.
    - Si max_pages_per_pack est défini → split en volumes :
        projet_context_20240101_120000_part1.pdf
        projet_context_20240101_120000_part2.pdf
        ...

    Retourne la liste des chemins générés.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        HRFlowable, Preformatted,
    )
    from reportlab.lib.enums import TA_CENTER

    project_name = project_path.resolve().name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    PAGE_W, PAGE_H = A4

    # ── Palette & styles ──
    palette = {
        "bg_header": colors.HexColor("#1a1a2e"),
        "accent":    colors.HexColor("#4361ee"),
        "accent2":   colors.HexColor("#7209b7"),
        "code_bg":   colors.HexColor("#f8f9fa"),
        "code_text": colors.HexColor("#212529"),
        "muted":     colors.HexColor("#6c757d"),
        "white":     colors.white,
        "hr":        colors.HexColor("#dee2e6"),
    }

    styles = getSampleStyleSheet()

    def make_styles():
        return {
            "title": ParagraphStyle(
                "CPTitle", parent=styles["Title"],
                fontSize=24, textColor=palette["white"],
                spaceAfter=6, fontName="Helvetica-Bold", alignment=TA_CENTER,
            ),
            "subtitle": ParagraphStyle(
                "CPSubtitle", parent=styles["Normal"],
                fontSize=10, textColor=colors.HexColor("#adb5bd"),
                spaceAfter=4, fontName="Helvetica", alignment=TA_CENTER,
            ),
            "h1": ParagraphStyle(
                "CPH1", parent=styles["Heading1"],
                fontSize=14, textColor=palette["accent"],
                spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold",
            ),
            "h2": ParagraphStyle(
                "CPH2", parent=styles["Heading2"],
                fontSize=11, textColor=palette["bg_header"],
                spaceBefore=8, spaceAfter=4, fontName="Helvetica-Bold",
            ),
            "file_header": ParagraphStyle(
                "CPFileHeader", parent=styles["Normal"],
                fontSize=12, textColor=palette["white"],
                fontName="Helvetica-Bold", spaceAfter=2,
                backColor=palette["accent"], borderPad=6, leftIndent=4,
            ),
            "meta": ParagraphStyle(
                "CPMeta", parent=styles["Normal"],
                fontSize=8, textColor=palette["muted"],
                fontName="Helvetica", spaceAfter=4,
            ),
            "body": ParagraphStyle(
                "CPBody", parent=styles["Normal"],
                fontSize=9, textColor=colors.HexColor("#212529"),
                fontName="Helvetica", spaceAfter=4, leading=14,
            ),
            "code": ParagraphStyle(
                "CPCode", parent=styles["Code"],
                fontSize=7.5, fontName="Courier",
                textColor=palette["code_text"], backColor=palette["code_bg"],
                borderPad=6, spaceAfter=4, leading=11,
                leftIndent=6, rightIndent=6,
            ),
            "toc_item": ParagraphStyle(
                "CPTocItem", parent=styles["Normal"],
                fontSize=9, fontName="Helvetica",
                spaceAfter=2, leftIndent=12,
                textColor=colors.HexColor("#495057"),
            ),
            "summary": ParagraphStyle(
                "CPSummary", parent=styles["Normal"],
                fontSize=9, fontName="Helvetica",
                spaceAfter=6, leading=14,
                textColor=colors.HexColor("#212529"),
            ),
        }

    def on_page_factory(proj_name, part_label=""):
        def on_page(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 7)
            canvas.setFillColor(palette["muted"])
            label = f"ContextPack — {proj_name}"
            if part_label:
                label += f"  •  {part_label}"
            canvas.drawString(1.5 * cm, 0.8 * cm, label)
            canvas.drawRightString(PAGE_W - 1.5 * cm, 0.8 * cm, f"Page {doc.page}")
            canvas.setStrokeColor(palette["hr"])
            canvas.setLineWidth(0.5)
            canvas.line(1.5 * cm, 1.2 * cm, PAGE_W - 1.5 * cm, 1.2 * cm)
            canvas.restoreState()
        return on_page

    total_size   = sum(f["size"] for f in files)
    total_tokens = sum(f.get("tokens", 0) for f in files)

    # ── Construire tous les éléments story (sans limite de pages) ──
    def build_cover(st, part_info=""):
        story = []
        story.append(Spacer(1, 3 * cm))
        story.append(Paragraph("🧠 ContextPack", st["title"]))
        story.append(Paragraph(project_name, ParagraphStyle(
            "CPProjectName2", parent=st["title"],
            fontSize=18, textColor=palette["accent"],
        )))
        if part_info:
            story.append(Paragraph(part_info, ParagraphStyle(
                "CPPartInfo", parent=st["subtitle"],
                fontSize=13, textColor=palette["accent2"],
            )))
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph(
            f"Pack de contexte IA — {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            st["subtitle"],
        ))
        story.append(Paragraph(
            f"{len(files)} fichiers • {total_size / 1024:.1f} Ko • ~{total_tokens:,} tokens estimés",
            st["subtitle"],
        ))
        story.append(Spacer(1, 1 * cm))
        story.append(HRFlowable(width="80%", thickness=2, color=palette["accent"], spaceAfter=8))
        story.append(PageBreak())
        return story

    def build_toc(st, file_list):
        story = []
        story.append(Paragraph("📚 Table des matières", st["h1"]))
        story.append(HRFlowable(width="100%", thickness=1, color=palette["hr"], spaceAfter=8))
        if summary:
            story.append(Paragraph("→ Résumé IA du projet", st["toc_item"]))
        for i, f in enumerate(file_list, 1):
            story.append(Paragraph(f"{i:02d}. {f['rel_path']}", st["toc_item"]))
        story.append(PageBreak())
        return story

    def build_summary_section(st):
        story = []
        if not summary:
            return story
        story.append(Paragraph("🤖 Résumé IA du projet", st["h1"]))
        story.append(HRFlowable(width="100%", thickness=1, color=palette["hr"], spaceAfter=8))
        _render_markdown_summary(summary, story, st["summary"], st["h1"], st["h2"], palette)
        story.append(PageBreak())
        return story

    def build_file_block(st, f):
        block = []
        block.append(Paragraph(f"📄 {f['rel_path']}", st["file_header"]))
        size_kb = f["size"] / 1024
        tokens  = f.get("tokens", 0)
        block.append(Paragraph(
            f"Taille: {size_kb:.1f} Ko  •  Tokens: {tokens:,}  •  Langage: {f['language']}",
            st["meta"],
        ))
        block.append(HRFlowable(width="100%", thickness=0.5, color=palette["hr"], spaceAfter=4))
        safe_content = _escape_for_reportlab(f["content"])
        block.append(Preformatted(safe_content, st["code"]))
        block.append(Spacer(1, 0.3 * cm))
        block.append(HRFlowable(width="100%", thickness=1, color=palette["hr"], spaceAfter=4))
        block.append(PageBreak())
        return block

    # ── Comptage réel des pages via dry-run ReportLab ──
    def count_pages_dry_run(story_elements) -> int:
        """
        Lance un build ReportLab sur BytesIO pour obtenir le vrai nombre de pages.
        Beaucoup plus fiable que toute heuristique sur les lignes.
        """
        import io
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.lib.units import cm

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=1.5 * cm, rightMargin=1.5 * cm,
            topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        )
        page_count = [0]

        def count_page(canvas, doc):
            page_count[0] = doc.page

        doc.build(story_elements, onFirstPage=count_page, onLaterPages=count_page)
        return page_count[0]

    generated_paths = []
    st = make_styles()

    if max_pages_per_pack is None:
        # ── Mode simple : un seul PDF ──
        story = []
        story += build_cover(st)
        story += build_toc(st, files)
        story += build_summary_section(st)
        for f in files:
            story += build_file_block(st, f)

        out_path = out_dir / f"{project_name}_context_{timestamp}.pdf"
        _build_pdf(story, out_path, project_name, on_page_factory(project_name))
        generated_paths.append(out_path)

    else:
        # ── Mode multi-volumes — splitting basé sur le vrai comptage de pages ──
        #
        # Stratégie :
        #   1. Mesurer en dry-run les pages fixes (couverture + TOC vide + résumé)
        #   2. Pour chaque fichier, mesurer en dry-run son bloc seul
        #   3. Grouper les fichiers en volumes en respectant max_pages_per_pack
        #
        from rich.console import Console as RConsole
        rc = RConsole()

        rc.print("[dim]🔍 Mesure des pages réelles (dry-run)...[/dim]")

        # Pages fixes du volume 1 (couverture + TOC + résumé)
        dummy_cover_toc_summary = (
            build_cover(st) +
            build_toc(st, files) +   # TOC complet pour être conservateur
            build_summary_section(st)
        )
        fixed_pages_vol1 = count_pages_dry_run(dummy_cover_toc_summary)

        # Pages fixes des volumes suivants (couverture + TOC seul, pas de résumé)
        dummy_cover_toc = build_cover(st) + build_toc(st, [files[0]] if files else [])
        fixed_pages_other = count_pages_dry_run(dummy_cover_toc)

        rc.print(f"[dim]  Pages fixes vol.1 : {fixed_pages_vol1}  |  autres volumes : {fixed_pages_other}[/dim]")

        # Mesurer les pages de chaque fichier individuellement
        file_pages: List[int] = []
        for i, f in enumerate(files):
            block = build_file_block(st, f)
            pages = count_pages_dry_run(block)
            file_pages.append(pages)
            rc.print(f"[dim]  {f['rel_path']} → {pages} page(s)[/dim]")

        # Grouper en volumes
        volumes: List[List[int]] = []   # liste d'indices de fichiers par volume
        current_indices: List[int] = []
        current_pages = fixed_pages_vol1  # volume 1 commence avec les pages fixes vol1

        for i, fp in enumerate(file_pages):
            fixed = fixed_pages_vol1 if not volumes else fixed_pages_other
            if current_pages + fp > max_pages_per_pack and current_indices:
                volumes.append(current_indices)
                current_indices = [i]
                current_pages = fixed_pages_other + fp
            else:
                current_indices.append(i)
                current_pages += fp

        if current_indices:
            volumes.append(current_indices)

        total_parts = len(volumes)
        rc.print(f"[cyan]📦 {total_parts} volume(s) prévu(s)[/cyan]")

        for part_idx, indices in enumerate(volumes, 1):
            vol_files = [files[i] for i in indices]
            part_label = f"Volume {part_idx}/{total_parts}"

            story = []
            story += build_cover(st, part_info=part_label)
            story += build_toc(st, vol_files)
            if part_idx == 1:
                story += build_summary_section(st)
            for f in vol_files:
                story += build_file_block(st, f)

            suffix = f"_part{part_idx}" if total_parts > 1 else ""
            out_path = out_dir / f"{project_name}_context_{timestamp}{suffix}.pdf"

            # Compter les pages avant le build final (dry-run sur le vrai story du volume)
            vol_pages = count_pages_dry_run(story)

            _build_pdf(
                story, out_path, project_name,
                on_page_factory(project_name, part_label if total_parts > 1 else ""),
            )
            rc.print(f"[green]✅ {out_path.name}[/green] [dim]({vol_pages} pages)[/dim]")
            generated_paths.append(out_path)

    return generated_paths


def _build_pdf(story, out_path: Path, title: str, on_page_fn):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.units import cm

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title=f"ContextPack — {title}",
        author="ContextPack",
        subject="Pack de contexte IA",
    )
    doc.build(story, onFirstPage=on_page_fn, onLaterPages=on_page_fn)


def _escape_for_reportlab(text: str) -> str:
    result = []
    for char in text:
        code = ord(char)
        if char in ("\n", "\t"):
            result.append(char)
        elif 32 <= code <= 126:
            result.append(char)
        elif code > 127:
            try:
                char.encode("latin-1")
                result.append(char)
            except (UnicodeEncodeError, UnicodeDecodeError):
                result.append("?")
        else:
            result.append(" ")
    return "".join(result)


def _render_markdown_summary(summary, story, style_body, style_h1, style_h2, palette):
    from reportlab.platypus import HRFlowable, Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors

    style_h3 = ParagraphStyle(
        "CPH3x", parent=style_body,
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
            pass
        elif stripped.startswith(("- ", "* ")):
            story.append(Paragraph(f"• {_md_inline(stripped[2:])}", ParagraphStyle(
                "CPBulletx", parent=style_body, leftIndent=12, spaceAfter=2,
            )))
        elif stripped.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=1, color=palette["hr"], spaceAfter=6))
        else:
            story.append(Paragraph(_md_inline(stripped), style_body))


def _md_inline(text: str) -> str:
    import re
    text = _escape_for_reportlab(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*",     r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`",       r'<font name="Courier" size="8">\1</font>', text)
    return text