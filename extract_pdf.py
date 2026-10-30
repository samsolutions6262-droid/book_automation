"""
Extract text from a PDF book, page by page, and save to a JSON file.
Also extracts the PDF's table of contents (bookmarks) if available.

Usage:
    python extract_pdf.py <input_pdf_path> [output_json_path]

If output_json_path is omitted, it defaults to 'extracted_text.json'
in the same directory as the input PDF.
"""

import sys
import os
import json
import fitz  # PyMuPDF


def extract_pdf(pdf_path: str, output_path: str):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    # Extract table of contents (bookmarks) if available
    toc = doc.get_toc(simple=True)  # [[level, title, page_number], ...]
    toc_entries = []
    for level, title, page_num in toc:
        toc_entries.append({
            "level": level,
            "title": title,
            "page": page_num
        })

    # Extract text from each page
    pages = []
    for i in range(total_pages):
        page = doc[i]
        text = page.get_text("text")
        pages.append({
            "page_num": i + 1,
            "text": text.strip()
        })
        print(f"  Extracted page {i + 1}/{total_pages}", end="\r")

    doc.close()

    result = {
        "source_file": os.path.basename(pdf_path),
        "total_pages": total_pages,
        "toc": toc_entries,
        "pages": pages
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Extracted {total_pages} pages to: {output_path}")
    if toc_entries:
        print(f"Found {len(toc_entries)} TOC entries (chapters/sections).")
    else:
        print("No TOC/bookmarks found in PDF. Chapters will need manual detection.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <input_pdf_path> [output_json_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = os.path.join(os.path.dirname(pdf_path), "extracted_text.json")

    extract_pdf(pdf_path, output_path)
