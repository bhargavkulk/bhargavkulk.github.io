import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from mako.lookup import TemplateLookup


@dataclass
class Args:
    input: Path
    metadata: Path
    templates: Path
    output: Path
    extra: list[Path]


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
    parser.add_argument('input', type=existing_path)
    parser.add_argument('metadata', type=existing_path)
    parser.add_argument('templates', type=is_a_dir)
    parser.add_argument('output', type=Path)
    parser.add_argument('-e', '--extra', type=existing_path, nargs='+', action='append', default=[])

    parsed_args = vars(parser.parse_args())
    parsed_args['extra'] = [path for group in parsed_args['extra'] for path in group]
    return Args(**parsed_args)


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
        print(
            'template not found in metadata, simply copying over the HTML fragment to output.',
            file=sys.stderr,
        )
        shutil.copy2(args.input, args.output)
        return

    template_file = metadata['template']
    html_fragment = args.input.read_text(encoding='utf-8')
    template_metadata: dict[str, object] = dict(metadata)
    template_metadata['content'] = html_fragment
    template_metadata.setdefault('title', metadata.get('id', ''))

    for extra_path in args.extra:
        variable_name = extra_path.stem
        if variable_name in template_metadata:
            raise ValueError(f'extra metadata variable "{variable_name}" conflicts with page metadata')

        with extra_path.open('rb') as fp:
            template_metadata[variable_name] = json.load(fp)

    lookup = TemplateLookup(
        directories=[str(args.templates)],
        input_encoding='utf-8',
    )
    template = lookup.get_template(template_file)
    html = template.render(**template_metadata)
    args.output.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    main()
