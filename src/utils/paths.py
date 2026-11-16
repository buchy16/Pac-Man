import sys
from pathlib import Path

# parents[2] pour remonter l'arbo: paths.py -> utils -> src -> racine du projet
ROOT_DIR = Path(__file__).resolve().parents[2]


# pour les assets embarqués
def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        base_path = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    else:
        base_path = ROOT_DIR  # Ancrage absolu :D
    return base_path / relative_path

# pour l'argument donné par le joueur (fichier de config)
def resolve_path(arg: str) -> Path:
    given = Path(arg)
    # chemin fourni par le joueur
    if given.is_file():
        return given
    # sinon : ressource embarquée
    bundled = resource_path(arg)
    return bundled if bundled.is_file() else given
