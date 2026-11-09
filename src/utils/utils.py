from typing import TYPE_CHECKING
from enum import Enum
import random
import logging
from ..Mlx import mlx
from .sprites import DIGITS, ALPHA

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
    """Affiche tous les attributs de la config, un par ligne (debug)."""
    for attribute, value in config.__dict__.items():
        print(f"{attribute.capitalize()}: {value}")


def build_digit_img(nums: str) -> None:
    nb_tiles_width = len(nums)

    total_w = nb_tiles_width * DIGIT_IMG_SIZE
    total_h = DIGIT_IMG_SIZE
    img = mlx.get_tools().mlx_new_image(mlx.mlx_ptr, total_w, total_h)
    bg_addr, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(img)
    bytes_per_px = bg_bpp // 8
    x, y = 0, 0
    for i in range(nb_tiles_width):
        tile_img = DIGITS[nums[i]]
        tile_addr, _, tile_line, _ = (mlx.get_tools().
                                      mlx_get_data_addr(tile_img))
        row_bytes = DIGIT_IMG_SIZE * bytes_per_px
        for line in range(DIGIT_IMG_SIZE):
            src_start = line * tile_line
            src = tile_addr[src_start:src_start + row_bytes]
            dst_start = (y + line) * bg_line + x * bytes_per_px
            bg_addr[dst_start:dst_start + row_bytes] = src
        x += DIGIT_IMG_SIZE

    return (img)


def build_text_img(string: str) -> None:
    alpha_char = "abcdefghijklmnopqrstuvwxyz 0123456789"
    nb_tiles_width = len(string)

    total_w = nb_tiles_width * ALPHA_IMG_SIZE
    total_h = ALPHA_IMG_SIZE
    atals = ALPHA

    img = mlx.get_tools().mlx_new_image(mlx.mlx_ptr, total_w, total_h)
    bg_addr, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(img)
    atlas_addr, _, atlas_line, _ = (mlx.get_tools().mlx_get_data_addr(atals))
    print(atlas_line)
    bytes_per_px = bg_bpp // 8
    x = 0
    for i in range(nb_tiles_width):
        img_x = alpha_char.find(string[i]) % 6
        img_y = alpha_char.find(string[i]) // 6
        letter_pos = (img_y * 14) * atlas_line + (img_x * 14) * bytes_per_px

        row_bytes = ALPHA_IMG_SIZE * bytes_per_px
        for line in range(ALPHA_IMG_SIZE):
            src_start = letter_pos + (line * atlas_line)
            src = atlas_addr[src_start:src_start + row_bytes]
            dst_start = line * bg_line + x * bytes_per_px
            bg_addr[dst_start:dst_start + row_bytes] = src
        x += ALPHA_IMG_SIZE

    return (img)


def display_nums(x: int, y: int, window: str, nums: str) -> int:
    try:
        img = build_digit_img(nums)
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows[window],
            img,
            x - 7,
            y - 7
            )
    except (KeyError):
        logging.warning("ERROR WHILE DISPLAYING DIGITS")
    finally:
        return (x + (len(nums) * DIGIT_IMG_SIZE))


def display_string(x: int, y: int, window: str, string: str) -> int:
    # try:
    img = build_text_img(string.lower())
    mlx.get_tools().mlx_put_image_to_window(
        mlx.mlx_ptr,
        mlx.windows[window],
        img,
        x - 7,
        y - 7
        )
    # except (KeyError):
    #     logging.warning("ERROR WHILE DISPLAYING TEXTS")
    # finally:
    return (x + (len(string) * ALPHA_IMG_SIZE))


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
    i = random.randint(0, nb_row - 1)
    j = random.randint(0, nb_col - 1)
    return (i, j)


def not_closed_cell(maze: "Maze", i: int, j: int) -> bool:
    # explicit conversion for MyPy
    return bool(maze._maze[i][j] != 15)


def random_open_cell(maze: "Maze") -> tuple[int, int]:
    while True:
        i, j = random_cell(maze._width, maze._height)
        if not_closed_cell(maze, i, j):
            return (i, j)
