from pathlib import Path


def Folder(pathlike: str | Path) -> Path:
    path = Path(pathlike)
    if not path.is_dir():
        raise NotADirectoryError(f'{path} is not a directory')
    return path
