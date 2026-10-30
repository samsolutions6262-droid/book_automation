"""
Merge page summaries into the template JSON, producing the final summaries.json.

Input: a JSON file mapping page numbers to summary strings:
    {"1": "summary text", "2": "summary text", ...}

Usage:
    python merge_summaries.py <template_json> <summaries_input_json> <output_json>
"""

import sys
import json


def merge_summaries(template_path: str, summaries_path: str, output_path: str):
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)

    with open(summaries_path, "r", encoding="utf-8") as f:
        summaries = json.load(f)

    filled = 0
    total = 0
    for chapter in template["chapters"]:
        for item in chapter["summaries"]:
            total += 1
            page_key = str(item["page"])
            if page_key in summaries and summaries[page_key].strip():
                item["summary"] = summaries[page_key].strip()
                filled += 1

    template["synthesis"] = summaries.get("__synthesis__", template.get("synthesis", ""))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print(f"Merged: {filled}/{total} summaries filled. Output: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python merge_summaries.py <template_json> <summaries_input_json> <output_json>")
        sys.exit(1)
    merge_summaries(sys.argv[1], sys.argv[2], sys.argv[3])
