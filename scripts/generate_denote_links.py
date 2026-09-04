import argparse
import json
import re
from pathlib import Path


DENOTE_IDENTIFIER = re.compile(r'^(\d{8}T\d{6})(?:--|$)')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('content_root', type=Path)
    parser.add_argument('sources', type=Path, nargs='*')
    return parser.parse_args()


def generate_links(content_root: Path, sources: list[Path]) -> dict[str, str]:
    links: dict[str, str] = {}

    for source in sources:
        match = DENOTE_IDENTIFIER.match(source.stem)
        if match is None:
            continue

        identifier = match.group(1)
        if identifier in links:
            raise ValueError(f'Duplicate Denote identifier {identifier}.')

        path = source.relative_to(content_root).with_suffix('.html')
        links[identifier] = '/' + path.as_posix()

    return links


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    links = generate_links(args.content_root, args.sources)

    args.output.write_text(
        json.dumps({'denote-links': links}, sort_keys=True),
        encoding='utf-8',
    )


if __name__ == '__main__':
    main()
