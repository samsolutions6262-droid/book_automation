"""
Split extracted text JSON into batch text files for AI processing.
Each batch covers a range of pages and is saved as a separate .txt file.

Usage:
    python split_batches.py <extracted_json_path> <batch_size> <output_dir>
"""

import sys
import os
import json


def split_batches(extracted_path: str, batch_size: int, output_dir: str):
    with open(extracted_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pages = data["pages"]
    total = len(pages)
    os.makedirs(output_dir, exist_ok=True)

    batch_num = 0
    for start in range(0, total, batch_size):
        batch_num += 1
        end = min(start + batch_size, total)
        batch_pages = pages[start:end]

        lines = []
        for p in batch_pages:
            lines.append(f"=== PAGE {p['page_num']} ===")
            lines.append(p["text"] if p["text"] else "[This page appears to be blank or contains only images]")
            lines.append("")

        batch_text = "\n".join(lines)
        batch_file = os.path.join(output_dir, f"batch_{batch_num:03d}.txt")
        with open(batch_file, "w", encoding="utf-8") as f:
            f.write(batch_text)

        first_page = batch_pages[0]["page_num"]
        last_page = batch_pages[-1]["page_num"]
        print(f"  Batch {batch_num}: pages {first_page}-{last_page} -> {batch_file}")

    print(f"\nDone! {batch_num} batches created in: {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python split_batches.py <extracted_json_path> <batch_size> <output_dir>")
        sys.exit(1)

    extracted_path = sys.argv[1]
    batch_size = int(sys.argv[2])
    output_dir = sys.argv[3]
    split_batches(extracted_path, batch_size, output_dir)
