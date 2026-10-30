"""
Append or update page summaries in a master summaries JSON file.
Creates the file if it doesn't exist.

Usage:
    python append_summaries.py <master_json> <new_summaries_json>

new_summaries_json format: {"1": "summary...", "2": "summary...", "__synthesis__": "..."}
"""

import sys
import json
import os


def append_summaries(master_path: str, new_path: str):
    if os.path.isfile(master_path):
        with open(master_path, "r", encoding="utf-8") as f:
            master = json.load(f)
    else:
        master = {}

    with open(new_path, "r", encoding="utf-8") as f:
        new = json.load(f)

    for key, value in new.items():
        master[key] = value

    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    count = sum(1 for k in master if k != "__synthesis__")
    print(f"Master now has {count} page summaries. Saved to: {master_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python append_summaries.py <master_json> <new_summaries_json>")
        sys.exit(1)
    append_summaries(sys.argv[1], sys.argv[2])
