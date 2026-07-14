#!/usr/bin/env python3
"""
generate_report_pdf.py
-----------------------
Erzeugt den finalen SEO-Kurzanalyse-Report als PDF, inklusive:
- Score-Gauge-Chart (0-1000, Farbzonen rot/gelb/gruen)
- Kategorie-Balkendiagramm (erreichte vs. moegliche Punkte je Kategorie)
- Zusammenfassung, priorisierte Handlungsempfehlungen
- Text-Swap-Tabelle (Ist-Text -> Neu-Text bzw. "an Stelle XY einfuegen" fuer neue Textbausteine)

Nutzung (aus einem anderen Skript/Claude-Workflow heraus):
    from generate_report_pdf import build_report, build_summary_report
    build_report(data, output_path="/mnt/user-data/outputs/seo-report-<url>.pdf")

Bei einer Website-weiten Analyse (mehrere URLs) wird zusaetzlich ein kurzes uebergreifendes
Executive-Summary-PDF erzeugt (feste Regel, siehe SKILL.md Schritt 7):
    build_summary_report(summary_data, output_path="/mnt/user-data/outputs/seo-summary-<domain>.pdf")

`data` ist ein Dict nach dem Schema, das im Modul-Docstring von `build_report` beschrieben ist.
`summary_data` folgt dem Schema im Docstring von `build_summary_report`.
Siehe auch `EXAMPLE_DATA` / `SUMMARY_EXAMPLE_DATA` unten fuer lauffaehige Beispiele
(python generate_report_pdf.py).

Abhaengigkeiten: reportlab, matplotlib (beide ueblicherweise vorinstalliert; sonst:
pip install reportlab matplotlib --break-system-packages)
"""

import os
import sys
import tempfile
import traceback
from datetime import datetime

# Muss synchron mit dem `version:`-Feld im Frontmatter von SKILL.md und mit CHANGELOG.md
# gehalten werden (siehe references/20-pflege-und-versionierung.md, Abschnitt
# "Skill-Versionierung").
SKILL_VERSION = "1.1.0"

try:
    import matplotlib
    matplotlib.use("Agg")  # kein Display noetig
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
        PageBreak, HRFlowable, KeepTogether,
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
except ImportError as e:
    raise SystemExit(
        "reportlab ist erforderlich. Installieren mit: "
        "pip install reportlab --break-system-packages"
    ) from e


# ---------------------------------------------------------------------------
# Farbdefinitionen (konsistent mit dem Ampel-System des Skills)
# ---------------------------------------------------------------------------
COLOR_RED = "#D64545"
COLOR_YELLOW = "#E8B93B"
COLOR_GREEN = "#3FA34D"
COLOR_DARK = "#1F2937"
COLOR_GREY = "#6B7280"
COLOR_ACCENT = "#2457C5"


def _score_color(score, max_score=1000):
    """Gibt die Ampelfarbe fuer einen gegebenen Score zurueck (fuer konsistente Faerbung)."""
    pct = score / max_score if max_score else 0
    if pct >= 0.75:
        return COLOR_GREEN
    if pct >= 0.55:
        return COLOR_YELLOW
    return COLOR_RED


def _build_gauge_chart(score, max_score=1000, out_path=None):
    """
    Erstellt ein Halbkreis-Gauge-Diagramm (Tacho-Optik) mit drei Farbzonen und einer
    Nadel/Markierung am aktuellen Score. Gibt den Dateipfad des erzeugten PNGs zurueck,
    oder None, wenn matplotlib nicht verfuegbar ist (Fallback: Report wird ohne Diagramm
    erzeugt, statt den ganzen Lauf abzubrechen).
    """
    if not MATPLOTLIB_OK:
        return None

    if out_path is None:
        out_path = tempfile.mktemp(suffix="_gauge.png")

    try:
        fig, ax = plt.subplots(figsize=(6, 3.6), subplot_kw={"aspect": "equal"})

        # Farbzonen als Halbkreis-Segmente (0-1000 auf 180-0 Grad gemappt)
        zones = [
            (0, 549, COLOR_RED),
            (549, 749, COLOR_YELLOW),
            (749, 1000, COLOR_GREEN),
        ]
        radius = 1.0
        width = 0.35
        for start, end, color in zones:
            theta1 = 180 - (start / max_score) * 180
            theta2 = 180 - (end / max_score) * 180
            wedge = matplotlib.patches.Wedge(
                (0, 0), radius, theta2, theta1, width=width,
                facecolor=color, edgecolor="white", linewidth=2,
            )
            ax.add_patch(wedge)

        # Nadel / Zeiger auf den aktuellen Score
        angle_deg = 180 - (min(score, max_score) / max_score) * 180
        angle_rad = np.deg2rad(angle_deg)
        needle_len = radius - width / 2
        x_tip = needle_len * np.cos(angle_rad)
        y_tip = needle_len * np.sin(angle_rad)
        ax.plot([0, x_tip], [0, y_tip], color=COLOR_DARK, linewidth=3, solid_capstyle="round")
        ax.add_patch(plt.Circle((0, 0), 0.045, color=COLOR_DARK, zorder=5))

        # Score-Text in der Mitte
        ax.text(0, -0.28, f"{int(round(score))}", ha="center", va="center",
                fontsize=34, fontweight="bold", color=COLOR_DARK)
        ax.text(0, -0.48, f"von {int(max_score)} Punkten", ha="center", va="center",
                fontsize=11, color=COLOR_GREY)

        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-0.65, 1.15)
        ax.axis("off")
        fig.tight_layout()
        fig.savefig(out_path, dpi=200, transparent=True)
        plt.close(fig)
        return out_path
    except Exception:
        # Diagramm ist ein Zusatznutzen, kein Grund den ganzen Report abzubrechen.
        traceback.print_exc()
        return None


def _build_category_bar_chart(kategorien, out_path=None):
    """
    Horizontales Balkendiagramm: erreichte vs. moegliche Punkte je Kategorie.
    kategorien: Liste von Dicts {"name": str, "erreicht": number, "max": number}
    Gibt den Dateipfad zurueck oder None bei Fehler/fehlendem matplotlib.
    """
    if not MATPLOTLIB_OK or not kategorien:
        return None

    if out_path is None:
        out_path = tempfile.mktemp(suffix="_kategorien.png")

    try:
        names = [k["name"] for k in kategorien][::-1]
        erreicht = [k["erreicht"] for k in kategorien][::-1]
        maxima = [k["max"] for k in kategorien][::-1]
        pct = [e / m if m else 0 for e, m in zip(erreicht, maxima)]
        bar_colors = [_score_color(e, m) for e, m in zip(erreicht, maxima)]

        fig, ax = plt.subplots(figsize=(6.4, 0.55 * len(names) + 0.8))
        y_pos = np.arange(len(names))

        # Hintergrund-Balken (max. moeglich, hellgrau) + Vordergrund-Balken (erreicht, farbig)
        ax.barh(y_pos, maxima, color="#E5E7EB", height=0.55, zorder=1)
        ax.barh(y_pos, erreicht, color=bar_colors, height=0.55, zorder=2)

        for i, (e, m) in enumerate(zip(erreicht, maxima)):
            ax.text(m + max(maxima) * 0.02, i, f"{int(e)}/{int(m)}",
                    va="center", ha="left", fontsize=9, color=COLOR_DARK)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(names, fontsize=10, color=COLOR_DARK)
        ax.set_xlim(0, max(maxima) * 1.18)
        ax.set_xticks([])
        for spine in ["top", "right", "bottom", "left"]:
            ax.spines[spine].set_visible(False)
        fig.tight_layout()
        fig.savefig(out_path, dpi=200, transparent=True)
        plt.close(fig)
        return out_path
    except Exception:
        traceback.print_exc()
        return None


def _draw_footer(canvas_obj, doc):
    """Zeichnet auf jeder Seite eine dezente Fußzeile mit Skill-Version, Seitenzahl und Datum."""
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColor(colors.HexColor(COLOR_GREY))
    footer_text = (
        f"SEO Ranking Experte v{SKILL_VERSION}  ·  "
        f"Erzeugt am {datetime.now().strftime('%d.%m.%Y')}  ·  Seite {doc.page}"
    )
    canvas_obj.drawCentredString(A4[0] / 2, 10 * mm, footer_text)
    canvas_obj.restoreState()


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle", fontSize=20, leading=24, textColor=colors.HexColor(COLOR_DARK),
        spaceAfter=4, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="ReportMeta", fontSize=9.5, leading=13, textColor=colors.HexColor(COLOR_GREY),
        spaceAfter=14,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading", fontSize=13.5, leading=17, textColor=colors.HexColor(COLOR_ACCENT),
        spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="SubHeading", fontSize=11, leading=14, textColor=colors.HexColor(COLOR_DARK),
        spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="BodySmall", fontSize=9.5, leading=13.5, textColor=colors.HexColor(COLOR_DARK),
    ))
    styles.add(ParagraphStyle(
        name="BodySmallGrey", fontSize=9, leading=12.5, textColor=colors.HexColor(COLOR_GREY),
    ))
    return styles


def _priority_table(items, styles, header_bg):
    """Baut eine Tabelle fuer eine Prioritaetsgruppe der Handlungsempfehlungen."""
    if not items:
        return Paragraph("Keine Punkte in dieser Kategorie.", styles["BodySmallGrey"])

    data = [["#", "Massnahme", "Warum", "Aufwand"]]
    for i, item in enumerate(items, 1):
        data.append([
            str(i),
            Paragraph(item.get("titel", ""), styles["BodySmall"]),
            Paragraph(item.get("begruendung", ""), styles["BodySmall"]),
            Paragraph(item.get("aufwand", ""), styles["BodySmall"]),
        ])

    table = Table(data, colWidths=[16, 130, 230, 55])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def _text_swap_table(swaps, styles):
    """
    Baut die Text-Swap-Tabelle. Jeder Eintrag hat "typ": "ersetzen" oder "neu".
    - "ersetzen": Ist-Text und Neu-Text nebeneinander, klar als Austausch gekennzeichnet.
    - "neu": kein Ist-Text vorhanden -> Hinweis "Diesen Text an Stelle <element> einfuegen".
    """
    if not swaps:
        return Paragraph("Keine Textaenderungen vorgeschlagen.", styles["BodySmallGrey"])

    flowables = []
    for i, swap in enumerate(swaps, 1):
        element = swap.get("element", f"Textstelle {i}")
        neu_text = swap.get("neu_text", "")
        begruendung = swap.get("begruendung", "")
        typ = swap.get("typ", "ersetzen")

        flowables.append(Paragraph(f"{i}. {element}", styles["SubHeading"]))

        if typ == "neu":
            hinweis = Paragraph(
                f'<b>Diesen Text an Stelle "{element}" einfügen:</b>', styles["BodySmall"]
            )
            neu_para = Paragraph(neu_text.replace("\n", "<br/>"), styles["BodySmall"])
            box = Table([[hinweis], [neu_para]], colWidths=[460])
            box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF2FF")),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor(COLOR_ACCENT)),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            flowables.append(box)
        else:
            ist_text = swap.get("ist_text", "")
            data = [
                [Paragraph("<b>Ist-Text (ersetzen)</b>", styles["BodySmallGrey"]),
                 Paragraph("<b>Neu-Text</b>", styles["BodySmallGrey"])],
                [Paragraph(ist_text.replace("\n", "<br/>"), styles["BodySmall"]),
                 Paragraph(neu_text.replace("\n", "<br/>"), styles["BodySmall"])],
            ]
            table = Table(data, colWidths=[230, 230])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            flowables.append(table)

        if begruendung:
            flowables.append(Spacer(1, 3))
            flowables.append(Paragraph(f"Begründung: {begruendung}", styles["BodySmallGrey"]))
        flowables.append(Spacer(1, 12))

    return KeepTogether(flowables[:1]) and flowables  # einzelne Eintraege duerfen umbrechen


def build_report(data, output_path):
    """
    Baut den vollstaendigen PDF-Report.

    Erwartetes Schema von `data` (fehlende Felder werden mit Platzhaltern aufgefuellt,
    das Skript bricht nicht ab, wenn einzelne optionale Felder fehlen):
    {
        "url": str,
        "datum": str (optional, sonst wird heutiges Datum verwendet),
        "gesamtscore": int (0-1000),
        "einordnung": str,
        "kategorien": [{"name": str, "erreicht": number, "max": number}, ...],
        "zusammenfassung": {"groesstes_risiko": str, "groesster_hebel": str},
        "empfehlungen": {
            "kritisch": [{"titel": str, "begruendung": str, "aufwand": str}, ...],
            "wichtig": [...],
            "optional": [...],
        },
        "text_swaps": [
            {"element": str, "typ": "ersetzen"|"neu", "ist_text": str (nur bei "ersetzen"),
             "neu_text": str, "begruendung": str},
            ...
        ],
        "annahmen_und_luecken": [str, ...],
    }
    """
    styles = _styles()
    story = []

    url = data.get("url", "unbekannte URL")
    datum = data.get("datum") or datetime.now().strftime("%d.%m.%Y")
    score = data.get("gesamtscore", 0)
    einordnung = data.get("einordnung", "")
    kategorien = data.get("kategorien", [])

    # --- Kopfbereich -------------------------------------------------------
    story.append(Paragraph("SEO-Ranking-Analyse", styles["ReportTitle"]))
    story.append(Paragraph(f"{url} &nbsp;|&nbsp; Erstellt am {datum}", styles["ReportMeta"]))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#E5E7EB"), thickness=1))

    # --- Score-Gauge ---------------------------------------------------
    gauge_path = _build_gauge_chart(score)
    if gauge_path:
        story.append(Spacer(1, 6))
        story.append(Image(gauge_path, width=280, height=168, hAlign="CENTER"))
    else:
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            f'<font size="28" color="{_score_color(score)}"><b>{score} / 1000</b></font>',
            ParagraphStyle("ScoreFallback", parent=styles["ReportTitle"], alignment=TA_CENTER),
        ))

    if einordnung:
        story.append(Paragraph(f"<b>Einordnung:</b> {einordnung}",
                                ParagraphStyle("EinordnungCenter", parent=styles["BodySmall"],
                                               alignment=TA_CENTER)))

    # --- Kategorie-Balkendiagramm ------------------------------------------
    bar_path = _build_category_bar_chart(kategorien)
    if bar_path:
        story.append(Spacer(1, 10))
        story.append(Paragraph("Punkte nach Kategorie", styles["SectionHeading"]))
        story.append(Image(bar_path, width=440, height=440 * (0.55 * len(kategorien) + 0.8) / 6.4,
                            hAlign="CENTER"))

    # --- Zusammenfassung -----------------------------------------------------
    zusammenfassung = data.get("zusammenfassung", {})
    if zusammenfassung:
        story.append(Paragraph("Zusammenfassung", styles["SectionHeading"]))
        if zusammenfassung.get("groesstes_risiko"):
            story.append(Paragraph(
                f"<b>Größtes Risiko:</b> {zusammenfassung['groesstes_risiko']}",
                styles["BodySmall"]))
        if zusammenfassung.get("groesster_hebel"):
            story.append(Paragraph(
                f"<b>Größter Hebel:</b> {zusammenfassung['groesster_hebel']}",
                styles["BodySmall"]))

    # --- Handlungsempfehlungen ----------------------------------------------
    empfehlungen = data.get("empfehlungen", {})
    story.append(PageBreak())
    story.append(Paragraph("Priorisierte Handlungsempfehlungen", styles["SectionHeading"]))

    story.append(Paragraph("🔴 Kritisch (blockiert Ranking/Indexierung)", styles["SubHeading"]))
    story.append(_priority_table(empfehlungen.get("kritisch", []), styles, COLOR_RED))
    story.append(Spacer(1, 10))

    story.append(Paragraph("🟡 Wichtig (bremst Wachstum)", styles["SubHeading"]))
    story.append(_priority_table(empfehlungen.get("wichtig", []), styles, COLOR_YELLOW))
    story.append(Spacer(1, 10))

    story.append(Paragraph("🟢 Optional (Feinschliff)", styles["SubHeading"]))
    story.append(_priority_table(empfehlungen.get("optional", []), styles, COLOR_GREEN))

    # --- Text-Swap-Liste -----------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("Textänderungen zum direkten Austausch", styles["SectionHeading"]))
    story.append(Paragraph(
        "Bei Einträgen mit vorhandenem Ist-Text: den linken Text 1:1 durch den rechten ersetzen. "
        "Bei neuen Textbausteinen ohne Ist-Text: den Text an der angegebenen Stelle neu einfügen.",
        styles["BodySmallGrey"]))
    story.append(Spacer(1, 8))
    for flowable in _text_swap_table(data.get("text_swaps", []), styles):
        story.append(flowable)

    # --- Annahmen & Lücken -----------------------------------------------------
    annahmen = data.get("annahmen_und_luecken", [])
    if annahmen:
        story.append(PageBreak())
        story.append(Paragraph("Annahmen & offene Punkte", styles["SectionHeading"]))
        for a in annahmen:
            story.append(Paragraph(f"• {a}", styles["BodySmall"]))

    # --- Dokument bauen -----------------------------------------------------
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
        title="SEO-Ranking-Analyse", author="SEO Ranking Experte",
    )
    try:
        doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)
    except Exception as e:
        raise RuntimeError(f"PDF-Erstellung fehlgeschlagen: {e}") from e

    return output_path


def _summary_table(seiten, styles):
    """Baut die Uebersichtstabelle mit einer Zeile pro analysierter URL."""
    data = [["URL", "Score", "Einordnung", "Groesstes Risiko", "Groesster Hebel"]]
    for seite in seiten:
        score = seite.get("score", 0)
        data.append([
            Paragraph(seite.get("url", ""), styles["BodySmall"]),
            Paragraph(f'<font color="{_score_color(score)}"><b>{int(score)}</b></font>',
                      styles["BodySmall"]),
            Paragraph(seite.get("einordnung", ""), styles["BodySmall"]),
            Paragraph(seite.get("groesstes_risiko", ""), styles["BodySmall"]),
            Paragraph(seite.get("groesster_hebel", ""), styles["BodySmall"]),
        ])

    table = Table(data, colWidths=[95, 35, 80, 130, 130])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(COLOR_ACCENT)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def build_summary_report(data, output_path):
    """
    Baut das uebergreifende Executive-Summary-PDF fuer eine Website-weite Analyse (mehrere
    URLs). Wird IMMER zusaetzlich zu den einzelnen Voll-Reports pro URL erzeugt (siehe
    SKILL.md Schritt 7) - nie als Ersatz dafuer. Enthaelt keine Handlungsempfehlungen/
    Text-Swaps im Detail, die stehen in den jeweiligen Einzel-Reports.

    Erwartetes Schema von `data`:
    {
        "domain": str,
        "datum": str (optional, sonst heutiges Datum),
        "seiten": [
            {
                "url": str,
                "score": int (0-1000),
                "einordnung": str,
                "groesstes_risiko": str,
                "groesster_hebel": str,
            },
            ...
        ],
        "uebergreifende_erkenntnisse": [str, ...] (optional, z.B. Muster, die auf mehreren
            Seiten auftreten, etwa "Meta-Descriptions fehlen durchgaengig"),
    }
    """
    styles = _styles()
    story = []

    domain = data.get("domain", "unbekannte Domain")
    datum = data.get("datum") or datetime.now().strftime("%d.%m.%Y")
    seiten = data.get("seiten", [])

    story.append(Paragraph("SEO-Website-Analyse – Executive Summary", styles["ReportTitle"]))
    story.append(Paragraph(
        f"{domain} &nbsp;|&nbsp; {len(seiten)} analysierte Seiten &nbsp;|&nbsp; "
        f"Erstellt am {datum}", styles["ReportMeta"]))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#E5E7EB"), thickness=1))

    if seiten:
        kategorien_fuer_chart = [
            {"name": s.get("url", "")[:40], "erreicht": s.get("score", 0), "max": 1000}
            for s in seiten
        ]
        bar_path = _build_category_bar_chart(kategorien_fuer_chart)
        if bar_path:
            story.append(Spacer(1, 10))
            story.append(Paragraph("Score im Vergleich", styles["SectionHeading"]))
            story.append(Image(
                bar_path, width=440,
                height=440 * (0.55 * len(kategorien_fuer_chart) + 0.8) / 6.4,
                hAlign="CENTER"))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Übersicht je Seite", styles["SectionHeading"]))
    story.append(_summary_table(seiten, styles))

    erkenntnisse = data.get("uebergreifende_erkenntnisse", [])
    if erkenntnisse:
        story.append(Spacer(1, 14))
        story.append(Paragraph("Übergreifende Erkenntnisse", styles["SectionHeading"]))
        for e in erkenntnisse:
            story.append(Paragraph(f"• {e}", styles["BodySmall"]))

    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "Detaillierte Handlungsempfehlungen und Text-Swap-Listen je Seite finden sich in den "
        "jeweiligen Einzel-Reports (ein PDF pro URL).", styles["BodySmallGrey"]))

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
        title="SEO-Website-Analyse – Executive Summary", author="SEO Ranking Experte",
    )
    try:
        doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)
    except Exception as e:
        raise RuntimeError(f"PDF-Erstellung fehlgeschlagen: {e}") from e

    return output_path


# ---------------------------------------------------------------------------
# Beispiel-Daten zum Testen: python generate_report_pdf.py
# ---------------------------------------------------------------------------
EXAMPLE_DATA = {
    "url": "https://beispiel-domain.de/leistungen",
    "gesamtscore": 837,
    "einordnung": "Gut – punktuelle Optimierungen sinnvoll",
    "kategorien": [
        {"name": "Crawling & Indexierung", "erreicht": 150, "max": 150},
        {"name": "Content & E-E-A-T", "erreicht": 240, "max": 300},
        {"name": "Page Experience/CWV", "erreicht": 120, "max": 150},
        {"name": "Strukturierte Daten", "erreicht": 75, "max": 100},
        {"name": "Spam-Freiheit", "erreicht": 100, "max": 100},
        {"name": "KI-Suche/GEO-Fitness", "erreicht": 152, "max": 200},
    ],
    "zusammenfassung": {
        "groesstes_risiko": "Fehlende Autor:innen-Angaben bei Ratgeberinhalten schwächen E-E-A-T.",
        "groesster_hebel": "Title-Tags und H1 klarer auf Suchintention ausrichten.",
    },
    "empfehlungen": {
        "kritisch": [],
        "wichtig": [
            {"titel": "Autor:innenboxen mit Fachexpertise ergänzen",
             "begruendung": "Stärkt E-E-A-T, besonders relevant bei Ratgeberinhalten.",
             "aufwand": "mittel"},
        ],
        "optional": [
            {"titel": "FAQ-Schema für Leistungsseiten ergänzen",
             "begruendung": "Erhöht Chance auf Rich-Result-Darstellung.",
             "aufwand": "niedrig"},
        ],
    },
    "text_swaps": [
        {"element": "Title-Tag", "typ": "ersetzen",
         "ist_text": "Leistungen - Beispiel GmbH",
         "neu_text": "SEO-Beratung für den Mittelstand | Beispiel GmbH",
         "begruendung": "Enthält jetzt das Ziel-Keyword und bleibt unter 60 Zeichen."},
        {"element": "Neuer Absatz am Ende von 'Über uns'", "typ": "neu",
         "neu_text": "Seit 2014 begleiten wir mittelständische Unternehmen ...",
         "begruendung": "Ergänzt fehlende Erfahrungs-/Vertrauenssignale (E-E-A-T)."},
    ],
    "annahmen_und_luecken": [
        "Keine Search-Console-Anbindung verfügbar – Klick-/Impressionsdaten fehlen.",
        "Zielgruppe wurde als 'B2B, KMU-Entscheider:innen' angenommen (nicht explizit bestätigt).",
    ],
}

SUMMARY_EXAMPLE_DATA = {
    "domain": "beispiel-domain.de",
    "seiten": [
        {"url": "https://beispiel-domain.de/", "score": 780,
         "einordnung": "Gut", "groesstes_risiko": "H1 fehlt.",
         "groesster_hebel": "Interne Verlinkung zu Leistungsseiten ausbauen."},
        {"url": "https://beispiel-domain.de/leistungen", "score": 837,
         "einordnung": "Gut", "groesstes_risiko": "Fehlende Autor:innen-Angaben.",
         "groesster_hebel": "Title-Tags klarer auf Suchintention ausrichten."},
        {"url": "https://beispiel-domain.de/blog/ratgeber-1", "score": 610,
         "einordnung": "Ausbaufähig", "groesstes_risiko": "Duenner Content, YMYL ohne E-E-A-T.",
         "groesster_hebel": "Fachexpertise und Quellenangaben ergänzen."},
    ],
    "uebergreifende_erkenntnisse": [
        "Meta-Descriptions fehlen auf mehreren Unterseiten durchgängig.",
        "Strukturierte Daten (Organization/LocalBusiness) sind nur auf der Startseite vorhanden.",
    ],
}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/seo-report-beispiel.pdf"
    path = build_report(EXAMPLE_DATA, out)
    print(f"Report erzeugt: {path}")

    summary_out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/seo-summary-beispiel.pdf"
    summary_path = build_summary_report(SUMMARY_EXAMPLE_DATA, summary_out)
    print(f"Summary-Report erzeugt: {summary_path}")
