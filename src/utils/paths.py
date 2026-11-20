import sys
from pathlib import Path

# parents[2] navigate up the directory tree: paths.py->utils->src->project root
ROOT_DIR = Path(__file__).resolve().parents[2]


# for embedded assets
def resource_path(relative_path: str) -> Path:
    """Path to a resource, both in development and in the PyInstaller build.
    ARG: name of the file being searched for
    RETURN: object from the `pathlib` module
    """
    if getattr(sys, "frozen", False):
        # in frozen mode, sys._MEIPASS points to dist/PacMan/_internal
        base_path = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    else:
        # in dev, absolute positioning
        base_path = ROOT_DIR
    return base_path / relative_path


# for the argument (configuration file) received via the console
def resolve_path(arg: str) -> Path:
    given = Path(arg)
    # path provided by the console is a valid file: we use it
    if given.is_file():
        return given
    # otherwise, we look for an embedded version
    bundled = resource_path(arg)
    # at worst, invalid original path will be handled by `get_valid_config()`,
    # which will revert to the default configuration.
    return bundled if bundled.is_file() else given
