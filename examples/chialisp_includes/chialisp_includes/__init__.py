from importlib.resources import files
from pathlib import Path


def include_directory() -> Path:
    return files(__package__) / "clib"
