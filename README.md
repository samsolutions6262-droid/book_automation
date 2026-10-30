# Book Automation — Page-by-Page PDF Summarizer

Automates the process of reading a full book PDF and producing a detailed,
page-by-page summary compiled into a clean, formatted output PDF.

## Workflow

```
[Upload PDF] → Step 1: Extract → Step 2: Summarize (AI) → Step 3: Generate PDF
```

### Step 1: Extract text from PDF

```bash
python extract_pdf.py "path/to/book.pdf"
```

Produces `extracted_text.json` containing:
- Source filename and total page count
- PDF table of contents (bookmarks) if available
- Full text of every page, in order

### Step 2: Create template & summarize

```bash
python create_template.py extracted_text.json
```

Produces `summaries_template.json` with chapter structure and empty summary slots.

Then, the AI (Cascade) reads through the extracted text and fills in:
- A 100–150 word summary for every page
- Chapter/section grouping
- An overall synthesis (key themes, narrative arc)

The completed file is saved as `summaries.json`.

### Step 3: Generate output PDF

```bash
python generate_pdf.py summaries.json
```

Produces `book_summary.pdf` with:
- Title page
- Table of contents
- Chapter headings with page-by-page summaries
- Overall synthesis section

## Requirements

```bash
pip install PyMuPDF reportlab
```

Python 3.8+
