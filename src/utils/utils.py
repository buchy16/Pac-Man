from typing import TYPE_CHECKING
from enum import Enum
import random
from .text_digit_displayer import DisplayString, DisplayNums

# parsing.py importe déjà utils.py, donc pour ne PAS créer d'import circulaire
# tout en fournissant les types 'GameConfig' et 'Maze' à VSCode et mypy,
# on utilise TYPE_CHECKING qui est toujours False à l'exécution :
if TYPE_CHECKING:
    from ..data.parse_config import GameConfig
    from ..game.maze import Maze

SPECIAL_CHAR = {
    "space": " ",
    "minus": "-",
    "KP_Insert": "0",
    "KP_End": "1",
    "KP_Down": "2",
    "KP_Page_Down": "3",
    "KP_Left": "4",
    "KP_Begin": "5",
    "KP_Right": "6",
    "KP_Home": "7",
    "KP_Up": "8",
    "KP_Page_Up": "9",
    "period": ".",
    "KP_Delete": "."
}

DIGIT_IMG_SIZE = 14
ALPHA_IMG_SIZE = 14


class Color(Enum):
    GREEN = "\033[32m"
    RED = "\033[31m"
    NONE = "\033[0m"


def print_green(msg: str, end_msg: str = '\n') -> None:
    """Print msg in green"""
    print(f"\033[32m{msg}\033[0m", end=end_msg)


def print_red(msg: str, end_msg: str = '\n') -> None:
    """Print msg in red"""
    print(f"\033[31m{msg}\033[0m", end=end_msg)


def print_config(config: "GameConfig") -> None:
    """Print all configuration attributes, one per line for debugging."""
    for attribute, value in config.__dict__.items():
        print(f"{attribute.capitalize()}: {value}")


def manhattan_dist(a: tuple[int, int], b: tuple[int, int]) -> int:
    """calculate the minimum number of squares between two cells, a and b
    parameters:
        a coordinates (i, j)
        b coordinates (i, j)
    Returns: estimated distance disregarding walls
            (number of squares in a row + number of squares in a column)
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def random_cell(nb_col: int, nb_row: int) -> tuple[int, int]:
    """Return random coordinates within the given grid dimensions.

    Args:
        nb_col: Number of columns in the grid.
        nb_row: Number of rows in the grid.

    Returns:
        A tuple containing the random row and column indices.
    """
    i = random.randint(0, nb_row - 1)
    j = random.randint(0, nb_col - 1)
    return (i, j)


def not_closed_cell(maze: "Maze", i: int, j: int) -> bool:
    """Return whether a maze cell is not completely closed.

    Args:
        maze: Maze containing the cell.
        i: Row index of the cell.
        j: Column index of the cell.

    Returns:
        True if the cell is open in at least one direction, otherwise False.
    """
    # explicit conversion for MyPy
    return bool(maze._maze[i][j] != 15)


def random_open_cell(maze: "Maze") -> tuple[int, int]:
    """Return random coordinates for an open cell in the maze.

    Args:
        maze: Maze from which to select an open cell.

    Returns:
        A tuple containing the row and column indices of an open cell.
    """
    while True:
        i, j = random_cell(maze._width, maze._height)
        if not_closed_cell(maze, i, j):
            return (i, j)


display_nums = DisplayNums()
display_string = DisplayString()
