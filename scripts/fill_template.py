import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from mako.lookup import TemplateLookup


@dataclass
class Args:
    metadata: Path
    templates: Path
    output: Path
    extra_metadata: list[Path]
    fragment: Path | None


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
    parser.add_argument('metadata', type=existing_path)
    parser.add_argument('templates', type=is_a_dir)
    parser.add_argument('output', type=Path)
    parser.add_argument('extra_metadata', type=existing_path, nargs='*')
    parser.add_argument('-f', '--fragment', type=existing_path)

    return Args(**vars(parser.parse_args()))


def main():
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.metadata.open('rb') as fp:
        metadata: dict[str, str] = json.load(fp)

    if 'content' in metadata:
        raise ValueError(
            'metadata of content file cannot use the key "content". This is reserved by the SSG.'
        )

    if 'template' not in metadata:
        if args.fragment is None:
            raise ValueError('cannot render page without a template or fragment')
        print(
            'template not found in metadata, simply copying over the HTML fragment to output.',
            file=sys.stderr,
        )
        shutil.copy2(args.fragment, args.output)
        return

    template_file = metadata['template']
    if args.fragment is not None:
        html_fragment = args.fragment.read_text(encoding='utf-8')
        metadata['content'] = html_fragment
    metadata.setdefault('title', metadata.get('id', ''))

    for extra_path in args.extra_metadata:
        variable_name = extra_path.stem
        if variable_name in metadata:
            raise ValueError(
                f'extra metadata variable "{variable_name}" conflicts with page metadata'
            )

        with extra_path.open('rb') as fp:
            metadata[variable_name] = json.load(fp)

    lookup = TemplateLookup(
        directories=[str(args.templates)],
        input_encoding='utf-8',
    )
    template = lookup.get_template(template_file)
    html = template.render(**metadata)
    args.output.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    main()
