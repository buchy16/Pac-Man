from typing import TYPE_CHECKING
from .Mlx import mlx
from .sprites import DIGITS

# parsing.py importe déjà utils.py, donc pour ne PAS créer d'import circulaire
# tout en fournissant le type de `config` à VSCode et mypy,
# on utilise TYPE_CHECKING qui est toujours False à l'exécution :
if TYPE_CHECKING:
    from .parse_config import GameConfig


def print_green(msg: str, end_msg: str = '\n') -> None:
    """Print msg in green"""
    print(f"\033[32m{msg}\033[0m", end=end_msg)


def print_red(msg: str, end_msg: str = '\n') -> None:
    """Print msg in red"""
    print(f"\033[31m{msg}\033[0m", end=end_msg)


def print_config(config: "GameConfig") -> None:
    """Affiche tous les attributs de la config, un par ligne (debug)."""
    for attribute, value in config.__dict__.items():
        print(f"{attribute.capitalize()}: {value}")


def display_nums(x: int, y: int, window: str, nums: str) -> int:
    for digit in nums:
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows[window],
            DIGITS[digit],
            x - 7,
            y - 7
        )
        x += 14
    return (x)
