import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from feedgen.feed import FeedGenerator


@dataclass
class Args:
    index: Path
    fragments: Path
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
    parser.add_argument('index', type=existing_path)
    parser.add_argument('fragments', type=is_a_dir)
    parser.add_argument('output', type=Path)

    return Args(**vars(parser.parse_args()))


URL = 'https://bhargavkulk.github.io/'


def main():
    args = parse_args()
    with args.index.open('rb') as fp:
        index: list[dict] = json.load(fp)
    fg = FeedGenerator()
    fg.id(URL)
    fg.title('Bhargav Kulkarni | Blog')
    fg.description('Blog posts from Bhargav Kulkarni.')
    fg.link(href=URL, rel='alternate')
    fg.author({'name': 'Bhargav Kulkarni', 'email': 'bhargavkishork@gmail.com'})
    for entry in index:
        feed_entry = fg.add_entry()
        feed_entry.id(URL + entry['path'])
        feed_entry.title(entry['title'])
        feed_entry.link(href=URL + entry['path'])

        post_html = Path('cache/' + entry['path']).read_text(encoding='utf-8')
        feed_entry.content(post_html, type='CDATA')

    args.output.mkdir(parents=True, exist_ok=True)
    atom_file = args.output / f'{args.index.stem}_atom.xml'
    rss_file = args.output / f'{args.index.stem}_rss.xml'
    fg.atom_file(str(atom_file))
    fg.rss_file(str(rss_file))


if __name__ == '__main__':
    main()
