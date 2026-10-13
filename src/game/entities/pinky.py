from ...directions import Direction
from .ghost import Ghost
from .player import Player
from ..maze import Maze
from ...utils import not_closed_cell
from ...directions import DIR_MOVES

"""
when CHASER
    Pinky is aiming to be MAGNETIC_DISTANCE squares ahead of Pacman
when FRIGHTENED
    ToDo
"""


class Pinky(Ghost):
    MAGNETIC_DISTANCE: int = 2

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(maze, player, prefix, speed,
                         i_start, j_start, dir_start)

        self.target = (self.player.i, self.player.j)

    def get_chase_target(self) -> tuple[int, int]:
        """determines the CHASER ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        nb_cells_forward = self.MAGNETIC_DISTANCE
        di, dj = DIR_MOVES.get(self.player.direction, (0, 0))
        max_row = self.maze._height - 1
        max_col = self.maze._width - 1

        # checks the cells from nb_cells_forward to 0 squares ahead the player
        for steps in range(nb_cells_forward, -1, -1):
            target_row = min(max(self.player.i + di * steps, 0), max_row)
            target_col = min(max(self.player.j + dj * steps, 0), max_col)

            if not_closed_cell(self.maze, target_row, target_col):
                return (target_row, target_col)

        # belt and suspenders :D
        return (self.player.i, self.player.j)

    def get_flee_target(self) -> tuple[int, int]:
        """determines the FRIGHTENED ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        # ToDo
        return (self.i_start, self.j_start)  # temp
