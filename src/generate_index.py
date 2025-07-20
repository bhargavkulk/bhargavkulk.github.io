#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except Exception:
        return datetime(1970, 1, 1)


def generate_index(input_folder, output_file, url_prefix):
    posts = []
    for json_file in Path(input_folder).glob("*.json"):
        if json_file.stem == "index":
            continue
        with open(json_file, encoding="utf-8") as f:
            meta = json.load(f)
            meta["slug"] = json_file.stem
            meta["url"] = f"{url_prefix}/{json_file.stem}.html"
            posts.append(meta)

    posts.sort(key=lambda m: parse_date(m.get("date", "01-01-1970")), reverse=True)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(posts, indent=2), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python3 src/generate_index.py <input_folder> <output_file> <url_prefix>"
        )
        sys.exit(1)

    input_folder = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    url_prefix = sys.argv[3].rstrip("/")

    generate_index(input_folder, output_file, url_prefix)
