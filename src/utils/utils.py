from typing import TYPE_CHECKING
import random
from ..Mlx import mlx
from .sprites import DIGITS

# parsing.py importe déjà utils.py, donc pour ne PAS créer d'import circulaire
# tout en fournissant les types 'GameConfig' et 'Maze' à VSCode et mypy,
# on utilise TYPE_CHECKING qui est toujours False à l'exécution :
if TYPE_CHECKING:
    from ..data.parse_config import GameConfig
    from ..game.maze import Maze


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


def manhattan_dist(a: tuple[int, int], b: tuple[int, int]) -> int:
    """calculate the minimum number of squares between two cells, a and b
    parameters:
        a coordinates (i, j)
        b coordinates (i, j)
    Returns: estimated distance disregarding walls
            (number of squares in a row + number of squares in a column)
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def random_cell(nb_col: int = 15, nb_row: int = 15) -> tuple[int, int]:
    i = random.randint(0, nb_col - 1)
    j = random.randint(0, nb_row - 1)
    return (i, j)


def not_closed_cell(maze: "Maze", i: int, j: int) -> bool:
    # explicit conversion for MyPy
    return bool(maze._maze[i][j] != 15)


def random_open_cell(maze: "Maze") -> tuple[int, int]:
    while True:
        i, j = random_cell()
        if not_closed_cell(maze, i, j):
            return (i, j)
