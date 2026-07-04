import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Args:
    output: Path
    entries: list[Path]


def existing_path(input: str) -> Path:
    path = Path(input)
    if not path.exists():
        raise argparse.ArgumentTypeError(f'{input} does not exist')
    return path


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('entries', type=existing_path, nargs='+')

    return Args(**vars(parser.parse_args()))


def main():
    args = parse_args()

    assert args.entries[0].is_dir(), f'{args.entries[0]} must be a dir'

    index_file = args.entries[0] / 'index.json'
    if not index_file.exists():
        raise ValueError(f'{args.entries[0]} does not contain an index.json')

    args.output.parent.mkdir(parents=True, exist_ok=True)

    collection_entries: list[dict[str, object]] = []

    for source_file in args.entries[1:]:
        if source_file.stem == 'index':
            continue

        with source_file.open('rb') as fp:
            entry = json.load(fp)

        entry['link'] = f'/{entry["path"]}'
        collection_entries.append(entry)

    with args.output.open('w', encoding='utf-8') as fp:
        json.dump(collection_entries, fp)


if __name__ == '__main__':
    main()
