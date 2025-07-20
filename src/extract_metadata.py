import json
import sys
from pathlib import Path


def extract_metadata(path):
    metadata = {"path": str(path)}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("="):
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    metadata["title"] = parts[1].strip()
                else:
                    metadata["title"] = ""
            elif line.startswith(":") and ":" in line[1:]:
                # Parse :key: value metadata line
                key, value = line[1:].split(":", 1)
                metadata[key.strip()] = value.strip()
            elif line == "":
                break  # end of metadata header
    if "date" not in metadata:
        raise ValueError(f"Missing required :date: metadata in {path}")
    return metadata


if __name__ == "__main__":
    for file in sys.argv[1:]:
        path = Path(file)
        meta = extract_metadata(path)
        relative = path.relative_to("content").with_suffix(".json")
        out_file = Path("cache") / relative
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
