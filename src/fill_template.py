import json
import sys
from pathlib import Path

from mako.lookup import TemplateLookup


def fill_template(template_folder, metadata_file, content_file, extra_metadata):
    lookup = TemplateLookup(directories=[template_folder])

    with open(metadata_file, encoding="utf-8") as f:
        metadata = json.load(f)

    for extra_file in extra_metadata:
        with open(extra_file, encoding="utf-8") as f:
            extra = json.load(f)
        key = extra_file.stem
        metadata[key] = extra

    with open(content_file, encoding="utf-8") as f:
        content_ = f.read()

    template_name = metadata.get("template", "base.html")
    template = lookup.get_template(template_name)

    return template.render(metadata=metadata, content_=content_)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Usage: python3 fill_template.py template_folder metadata.json content.html output.html [extra_metadata...]"
        )
        sys.exit(1)

    template_folder = Path(sys.argv[1])
    metadata_file = Path(sys.argv[2])
    content_file = Path(sys.argv[3])
    output_file = Path(sys.argv[4])
    extra_metadata = []
    if len(sys.argv) > 5:
        extra_metadata = [Path(f) for f in sys.argv[5:]]

    rendered = fill_template(
        template_folder, metadata_file, content_file, extra_metadata
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered)
