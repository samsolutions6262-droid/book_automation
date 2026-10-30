"""
Create a template summaries JSON from extracted text.
Uses the PDF's TOC if available, otherwise attempts heuristic chapter detection.
Summaries are left empty for the AI to fill in.

Usage:
    python create_template.py <extracted_json_path> [template_json_path]
"""

import sys
import os
import json
import re


def detect_chapters_heuristic(pages: list) -> list:
    """
    Attempt to detect chapter boundaries from page text.
    Looks for common chapter heading patterns on pages.
    """
    chapter_pattern = re.compile(
        r'^(?:CHAPTER|Chapter|CHAPTER\s+\d+|Chapter\s+\d+|CHAPTER\s+[IVXLC]+|Chapter\s+[IVXLC]+|PART|Part|PART\s+\d+|Part\s+\d+|PROLOGUE|EPILOGUE|INTRODUCTION|Introduction|PREFACE|Preface|ACKNOWLEDGMENTS|Contents|CONTENTS)',
        re.MULTILINE
    )

    chapters = []
    current_chapter = {"title": "Front Matter", "summaries": []}

    for page in pages:
        text = page["text"]
        page_num = page["page_num"]

        # Check first few lines for chapter heading
        lines = text.split("\n")[:5] if text else []
        first_lines = "\n".join(lines)

        match = chapter_pattern.search(first_lines)
        if match:
            # Save previous chapter if it has pages
            if current_chapter["summaries"]:
                chapters.append(current_chapter)
            # Start new chapter - use the matched line as title
            matched_line = match.group(0)
            # Try to get a fuller title from the line
            for line in lines:
                if matched_line in line:
                    current_chapter = {"title": line.strip(), "summaries": []}
                    break
            else:
                current_chapter = {"title": matched_line, "summaries": []}

        current_chapter["summaries"].append({"page": page_num, "summary": ""})

    if current_chapter["summaries"]:
        chapters.append(current_chapter)

    return chapters


def create_template(extracted_path: str, template_path: str):
    with open(extracted_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    source_file = data.get("source_file", "Unknown Book")
    total_pages = data.get("total_pages", 0)
    toc_entries = data.get("toc", [])
    pages = data.get("pages", [])

    if toc_entries:
        # Build chapters from TOC
        chapters = []
        for i, entry in enumerate(toc_entries):
            start_page = entry["page"]
            if i + 1 < len(toc_entries):
                end_page = toc_entries[i + 1]["page"] - 1
            else:
                end_page = total_pages

            chapter_pages = [p for p in pages if start_page <= p["page_num"] <= end_page]
            summaries = [{"page": p["page_num"], "summary": ""} for p in chapter_pages]

            chapters.append({
                "title": entry["title"],
                "summaries": summaries
            })
    else:
        # Heuristic detection
        chapters = detect_chapters_heuristic(pages)

    template = {
        "source_file": source_file,
        "total_pages": total_pages,
        "toc": toc_entries,
        "chapters": chapters,
        "synthesis": ""
    }

    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print(f"Template created: {template_path}")
    print(f"  Chapters detected: {len(chapters)}")
    print(f"  Total pages: {total_pages}")
    empty_summaries = sum(len(ch["summaries"]) for ch in chapters)
    print(f"  Summaries to fill: {empty_summaries}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_template.py <extracted_json_path> [template_json_path]")
        sys.exit(1)

    extracted_path = sys.argv[1]
    if not os.path.isfile(extracted_path):
        print(f"Error: File not found: {extracted_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        template_path = sys.argv[2]
    else:
        template_path = os.path.join(os.path.dirname(extracted_path), "summaries_template.json")

    create_template(extracted_path, template_path)
