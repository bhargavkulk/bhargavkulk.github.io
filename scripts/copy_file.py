import argparse
import shutil
from pathlib import Path


def existing_path(value: str) -> Path:
    path = Path(value)
    if not path.exists():
        raise argparse.ArgumentTypeError(f'{value} does not exist')
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=existing_path)
    parser.add_argument('output', type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.input, args.output)


if __name__ == '__main__':
    main()
