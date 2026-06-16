import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Args:
    collection: Path
    output: Path


def existing_path(input: str) -> Path:
    path = Path(input)
    if not path.exists():
        raise argparse.ArgumentTypeError(f'{input} does not exist')
    return path


def is_a_dir(input: str) -> Path:
    path = existing_path(input)
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f'{input} is not a directory')
    return path


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument('collection', type=is_a_dir)
    parser.add_argument('output', type=Path)

    return Args(**vars(parser.parse_args()))


def main():
    args = parse_args()
    index_file = args.collection / 'index.dj'
    if not index_file.exists():
        raise ValueError(f'{args.collection} does not contain an index.dj')

    args.output.parent.mkdir(parents=True, exist_ok=True)

    collection_entries: list[dict[str, object]] = []
    cache_dir = args.output.parent / args.collection.name

    for source_file in args.collection.iterdir():
        if source_file.name == 'index.dj' or source_file.suffix != '.dj' or not source_file.is_file():
            continue

        metadata_path = cache_dir / f'{source_file.stem}.json'
        with metadata_path.open('rb') as fp:
            entry = json.load(fp)

        entry['slug'] = source_file.stem
        entry['link'] = f'/{args.collection.name}/{source_file.stem}.html'
        collection_entries.append(entry)

    with args.output.open('w', encoding='utf-8') as fp:
        json.dump(collection_entries, fp)


if __name__ == '__main__':
    main()
