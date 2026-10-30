"""
Merge all batch summary JSON files and the overall synthesis into a final PDF.
"""
import json
import os
import glob
from fpdf import FPDF
import re

SUMMARIES_DIR = r"d:\Book Automation\summaries"
OUTPUT_PDF = r"d:\Book Automation\Think_and_Grow_Rich_Summaries.pdf"

# Collect all batch summary files
batch_files = sorted(glob.glob(os.path.join(SUMMARIES_DIR, "batch_*_summaries.json")))
print(f"Found {len(batch_files)} batch summary files")

# Load and merge all summaries
all_summaries = {}
for bf in batch_files:
    with open(bf, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for page_num, summary in data.items():
        all_summaries[int(page_num)] = summary

# Sort by page number
sorted_pages = sorted(all_summaries.keys())
print(f"Total pages summarized: {len(sorted_pages)} (pages {sorted_pages[0]}-{sorted_pages[-1]})")

# Load synthesis
synthesis_path = os.path.join(SUMMARIES_DIR, "overall_synthesis.json")
with open(synthesis_path, 'r', encoding='utf-8') as f:
    synthesis_data = json.load(f)

# Helper: replace common Unicode chars with ASCII equivalents
def clean_text(text):
    replacements = {
        '\u2014': '--',   # em dash
        '\u2013': '-',    # en dash
        '\u2019': "'",   # right single quote
        '\u2018': "'",   # left single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2026': '...',  # ellipsis
        '\u00e9': 'e',    # e acute
        '\u00e8': 'e',    # e grave
        '\u00f1': 'n',    # n tilde
        '\u00f3': 'o',    # o acute
        '\u00ed': 'i',    # i acute
        '\u00e1': 'a',    # a acute
        '\u00fc': 'u',    # u umlaut
        '\u00f6': 'o',    # o umlaut
        '\u00e4': 'a',    # a umlaut
        '\u00df': 'ss',   # sharp s
        '\u00e7': 'c',    # c cedilla
        '\u00ea': 'e',    # e circumflex
        '\u00ee': 'i',    # i circumflex
        '\u00f4': 'o',    # o circumflex
        '\u00fb': 'u',    # u circumflex
        '\u00e0': 'a',    # a grave
        '\u00f2': 'o',    # o grave
        '\u00f9': 'u',    # u grave
        '\u00e2': 'a',    # a circumflex
        '\u00ee': 'i',
        '\u00ef': 'i',
        '\u00eb': 'e',
        '\u00e8': 'e',
        '\u00e6': 'ae',
        '\u0153': 'oe',
        '\u0152': 'OE',
        '\u00c0': 'A',
        '\u00c1': 'A',
        '\u00c2': 'A',
        '\u00c3': 'A',
        '\u00c4': 'A',
        '\u00c5': 'A',
        '\u00c7': 'C',
        '\u00c8': 'E',
        '\u00c9': 'E',
        '\u00ca': 'E',
        '\u00cb': 'E',
        '\u00cc': 'I',
        '\u00cd': 'I',
        '\u00ce': 'I',
        '\u00cf': 'I',
        '\u00d1': 'N',
        '\u00d2': 'O',
        '\u00d3': 'O',
        '\u00d4': 'O',
        '\u00d5': 'O',
        '\u00d6': 'O',
        '\u00d9': 'U',
        '\u00da': 'U',
        '\u00db': 'U',
        '\u00dc': 'U',
        '\u00fd': 'y',
        '\u00ff': 'y',
        '\u00dd': 'Y',
        '\u00bf': '',      # inverted question mark
        '\u00a1': '',      # inverted exclamation mark
        '\u00ab': '"',
        '\u00bb': '"',
        '\u00b0': ' degrees',
        '\u00b2': '2',
        '\u00b3': '3',
        '\u00bd': '1/2',
        '\u00bc': '1/4',
        '\u00be': '3/4',
        '\u00a2': ' cents',
        '\u00a3': ' GBP',
        '\u00a5': ' Yen',
        '\u20ac': ' EUR',
        '\u00ae': '(R)',
        '\u00a9': '(C)',
        '\u2122': '(TM)',
        '\u00b7': '*',
        '\u00d7': 'x',
        '\u00f7': '/',
        '\u2192': '->',
        '\u2190': '<-',
        '\u2194': '<->',
    }
    for unicode_char, ascii_replacement in replacements.items():
        text = text.replace(unicode_char, ascii_replacement)
    # Remove any remaining non-latin1 chars
    text = text.encode('latin-1', errors='replace').decode('latin-1')
    return text

# Create PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=25)

# --- Title Page ---
pdf.add_page()
pdf.set_font("Helvetica", "B", 24)
pdf.multi_cell(0, 12, "Think and Grow Rich", align="C")
pdf.ln(5)
pdf.set_font("Helvetica", "B", 16)
pdf.multi_cell(0, 10, "Comprehensive Page-by-Page Summaries", align="C")
pdf.ln(3)
pdf.set_font("Helvetica", "I", 12)
pdf.multi_cell(0, 8, "by Napoleon Hill", align="C")
pdf.ln(3)
pdf.set_font("Helvetica", "", 10)
pdf.multi_cell(0, 6, "Revised and Expanded Edition\nEdited by Ross Cornwell", align="C")
pdf.ln(10)
pdf.set_font("Helvetica", "", 10)
pdf.multi_cell(0, 6, f"Summaries cover pages {sorted_pages[0]} through {sorted_pages[-1]}\nin {len(batch_files)} batches of 10 pages each.", align="C")
pdf.ln(20)
pdf.set_font("Helvetica", "I", 10)
pdf.multi_cell(0, 6, "Generated from detailed page-by-page analysis of the original text.", align="C")

# --- Table of Contents ---
pdf.add_page()
pdf.set_font("Helvetica", "B", 18)
pdf.multi_cell(0, 12, "Table of Contents", align="C")
pdf.ln(5)
pdf.set_font("Helvetica", "B", 12)
pdf.multi_cell(0, 8, "Overall Synthesis")
pdf.set_font("Helvetica", "", 10)
pdf.set_x(pdf.l_margin + 5)
pdf.multi_cell(0, 6, "A comprehensive overview of the book's 13 principles, themes, and structure.")
pdf.ln(3)

# Chapter/section mapping based on page ranges
sections = [
    (1, 6, "Author's Preface / Introduction"),
    (7, 20, "Chapter 1: DESIRE - The Starting Point of All Achievement"),
    (21, 44, "Chapter 2: FAITH - Visualization and the Attainment of Desire"),
    (45, 56, "Chapter 3: AUTOSUGGESTION - The Medium for Influencing the Subconscious Mind"),
    (57, 74, "Chapter 4: SPECIALIZED KNOWLEDGE - Personal Experiences or Observations"),
    (75, 90, "Chapter 5: IMAGINATION - The Workshop of the Mind"),
    (91, 124, "Chapter 6: ORGANIZED PLANNING - The Crystallization of Desire into Action"),
    (125, 148, "Chapter 7: DECISION - The Mastery of Procrastination"),
    (149, 162, "Chapter 8: PERSISTENCE - The Sustained Effort Necessary to Induce Faith"),
    (163, 170, "Chapter 9: POWER OF THE MASTER MIND - The Driving Force"),
    (171, 188, "Chapter 10: THE MYSTERY OF SEX TRANSMUTATION"),
    (189, 210, "Chapter 11: THE SUBCONSCIOUS MIND - The Connecting Link"),
    (211, 218, "Chapter 12: THE BRAIN - A Broadcasting and Receiving Station for Thought"),
    (219, 238, "Chapter 13: THE SIXTH SENSE - The Door to the Temple of Wisdom"),
    (239, 276, "Epilogue: HOW TO OUTWIT THE SIX GHOSTS OF FEAR"),
    (277, 280, "Appendix A: About the Author / Tributes"),
    (281, 284, "Appendix B: Tributes to the Author From Great American Leaders"),
    (285, 286, "Appendix C: Original Publisher's Preface"),
    (287, 289, "Appendix D: This Standing Army Is at Your Service"),
    (290, 292, "Appendix E: What Do You Want Most?"),
    (293, 298, "Appendix F: Early Sources"),
    (299, 299, "Appendix G: Works by Napoleon Hill"),
    (300, 301, "Appendix H: It Couldn't Be Done (poem)"),
    (302, 303, "Appendix I: The Mindpower Press"),
    (304, 307, "Acknowledgements"),
    (308, 371, "Endnotes"),
    (372, 385, "Index"),
    (386, 386, "Photo Section"),
    (387, 388, "About the Author / About the Editor"),
    (389, 397, "More Praise for Think and Grow Rich!"),
]

for start, end, title in sections:
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_x(pdf.l_margin + 5)
    pdf.multi_cell(0, 6, f"Pages {start}-{end}: {title}")

# --- Overall Synthesis ---
pdf.add_page()
pdf.set_font("Helvetica", "B", 18)
pdf.multi_cell(0, 12, "Overall Synthesis", align="C")
pdf.ln(5)
pdf.set_font("Helvetica", "", 10)
synthesis_text = synthesis_data.get("synthesis", "")
# Split into paragraphs
paragraphs = synthesis_text.split("\n\n")
for para in paragraphs:
    para = para.strip()
    if para:
        # Check if it's a section header (all caps or starts with a keyword)
        if para.isupper() or (len(para) < 100 and para.endswith(":")):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 5, clean_text(para))
            pdf.set_font("Helvetica", "", 10)
        else:
            pdf.multi_cell(0, 5, clean_text(para))
            pdf.ln(2)

# --- Page-by-Page Summaries ---
pdf.add_page()
pdf.set_font("Helvetica", "B", 18)
pdf.multi_cell(0, 12, "Page-by-Page Summaries", align="C")
pdf.ln(5)

for page_num in sorted_pages:
    summary = all_summaries[page_num]
    pdf.set_font("Helvetica", "B", 11)
    pdf.ln(2)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6, f"Page {page_num}")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_x(pdf.l_margin)
    try:
        pdf.multi_cell(0, 4.5, clean_text(summary))
    except Exception as e:
        print(f"  ERROR on page {page_num}: {e}")
        # Try with a narrower width and explicit word wrap
        text = clean_text(summary)
        # Break long words (>80 chars) into smaller pieces
        import textwrap
        wrapped = textwrap.fill(text, width=90, break_long_words=True, break_on_hyphens=True)
        pdf.multi_cell(0, 4.5, wrapped)
    pdf.ln(1)

# Save
pdf.output(OUTPUT_PDF)
print(f"PDF saved to: {OUTPUT_PDF}")
print(f"Total pages in PDF: {pdf.page_no()}")
