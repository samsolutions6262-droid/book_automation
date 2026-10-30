"""
Generate a formatted summary PDF from a summaries JSON file.

The summaries JSON should have this structure:
{
    "source_file": "book.pdf",
    "total_pages": 300,
    "toc": [
        {"level": 1, "title": "Chapter 1: Introduction", "page": 1},
        ...
    ],
    "chapters": [
        {
            "title": "Chapter 1: Introduction",
            "summaries": [
                {"page": 1, "summary": "..."},
                {"page": 2, "summary": "..."},
                ...
            ]
        },
        ...
    ],
    "synthesis": "Overall synthesis text..."
}

Usage:
    python generate_pdf.py <summaries_json_path> [output_pdf_path]

If output_pdf_path is omitted, defaults to 'book_summary.pdf' in the
same directory as the input JSON.
"""

import sys
import os
import json

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.lib import colors


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="BookTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=HexColor("#1a1a2e"),
    ))

    styles.add(ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        fontSize=12,
        leading=16,
        spaceAfter=6,
        alignment=TA_CENTER,
        textColor=HexColor("#666666"),
    ))

    styles.add(ParagraphStyle(
        name="TOCHeading",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        spaceBefore=20,
        spaceAfter=14,
        textColor=HexColor("#1a1a2e"),
    ))

    styles.add(ParagraphStyle(
        name="TOCEntry",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        leftIndent=20,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="ChapterTitle",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        spaceBefore=24,
        spaceAfter=14,
        textColor=HexColor("#1a1a2e"),
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        name="PageLabel",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        spaceBefore=12,
        spaceAfter=4,
        textColor=HexColor("#16213e"),
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        name="SummaryBody",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=15,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=HexColor("#222222"),
    ))

    styles.add(ParagraphStyle(
        name="SynthesisTitle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        spaceBefore=24,
        spaceAfter=14,
        textColor=HexColor("#1a1a2e"),
    ))

    styles.add(ParagraphStyle(
        name="SynthesisBody",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=HexColor("#222222"),
    ))

    return styles


def generate_pdf(summaries_path: str, output_path: str):
    with open(summaries_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    source_file = data.get("source_file", "Unknown Book")
    total_pages = data.get("total_pages", 0)
    toc_entries = data.get("toc", [])
    chapters = data.get("chapters", [])
    synthesis = data.get("synthesis", "")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title=f"Summary: {source_file}",
        author="Book Automation",
    )

    styles = build_styles()
    story = []

    # --- Title Page ---
    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph(f"Summary of", styles["Subtitle"]))
    story.append(Paragraph(source_file, styles["BookTitle"]))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(f"Page-by-page summary covering {total_pages} pages", styles["Subtitle"]))
    story.append(PageBreak())

    # --- Table of Contents ---
    story.append(Paragraph("Table of Contents", styles["TOCHeading"]))
    story.append(Spacer(1, 0.5 * cm))

    if toc_entries:
        for entry in toc_entries:
            indent = (entry.get("level", 1) - 1) * 20
            title = entry.get("title", "Untitled")
            page = entry.get("page", "?")
            toc_text = f"{title} <font color='#888888'>............ p. {page}</font>"
            style = ParagraphStyle(
                name=f"TOCLevel{entry.get('level', 1)}",
                parent=styles["TOCEntry"],
                leftIndent=indent,
                fontSize=12 - (entry.get("level", 1) - 1),
            )
            story.append(Paragraph(toc_text, style))
    elif chapters:
        for ch in chapters:
            title = ch.get("title", "Untitled")
            page_range = ""
            sums = ch.get("summaries", [])
            if sums:
                first_p = sums[0].get("page", "?")
                last_p = sums[-1].get("page", "?")
                page_range = f" (pp. {first_p}-{last_p})" if first_p != last_p else f" (p. {first_p})"
            story.append(Paragraph(f"{title}{page_range}", styles["TOCEntry"]))
    else:
        story.append(Paragraph("(No table of contents available)", styles["TOCEntry"]))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("Overall Synthesis <font color='#888888'>............ see end</font>", styles["TOCEntry"]))
    story.append(PageBreak())

    # --- Chapter Summaries ---
    for chapter in chapters:
        ch_title = chapter.get("title", "Untitled Section")
        story.append(Paragraph(ch_title, styles["ChapterTitle"]))

        for item in chapter.get("summaries", []):
            page_num = item.get("page", "?")
            summary_text = item.get("summary", "")

            label = Paragraph(f"Page {page_num}:", styles["PageLabel"])
            body = Paragraph(summary_text, styles["SummaryBody"])
            story.append(KeepTogether([label, body]))

        story.append(Spacer(1, 0.5 * cm))

    # --- Synthesis ---
    story.append(PageBreak())
    story.append(Paragraph("Overall Synthesis", styles["SynthesisTitle"]))
    if synthesis:
        for para in synthesis.split("\n\n"):
            if para.strip():
                story.append(Paragraph(para.strip(), styles["SynthesisBody"]))
    else:
        story.append(Paragraph("(Synthesis not provided)", styles["SynthesisBody"]))

    doc.build(story)
    print(f"Done! Summary PDF generated: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_pdf.py <summaries_json_path> [output_pdf_path]")
        sys.exit(1)

    summaries_path = sys.argv[1]
    if not os.path.isfile(summaries_path):
        print(f"Error: File not found: {summaries_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = os.path.join(os.path.dirname(summaries_path), "book_summary.pdf")

    generate_pdf(summaries_path, output_path)
