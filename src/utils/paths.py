import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]


def resource_path(relative_path: str) -> Path:
    """Path to a resource, both in development and in the PyInstaller build.
    ARG: name of the file being searched for
    RETURN: object from the `pathlib` module
    """
    if getattr(sys, "frozen", False):
        base_path = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    else:
        base_path = ROOT_DIR
    return base_path / relative_path


def resolve_path(arg: str) -> Path:
    """Resolve the configuration file path received from the command line.
    Lookup order:
      1. the path given by the user, if it is an existing file;
      2. an embedded version of it;
      3. the original and invalid path,
         `get_valid_config()` will fall back to the default configuration.

    ARG: path or file name of the configuration file given in the console
    RETURN: object from the `pathlib` module
    """
    given = Path(arg)
    if given.is_file():
        return given
    bundled = resource_path(arg)
    return bundled if bundled.is_file() else given
