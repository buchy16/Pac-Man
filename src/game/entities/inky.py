from ...utils.directions import Direction
from .ghost import Ghost
from .player import Player
from ..maze import Maze
from ...utils.utils import random_open_cell

"""
when CHASER
    Inky moves randomly
when FRIGHTENED
    Inky moves to the corner furthest from Pac-Man
    This target is updated when it is reached,
    or if Pac-Man has entered the same quarter of the maze as the target
"""


class Inky(Ghost):
    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(maze, player, prefix, speed,
                         i_start, j_start, dir_start)

        self.target = (self.i_start, self.j_start)

    def get_chase_target(self) -> tuple[int, int]:
        """determines the CHASER ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        inky_coord = (self.i, self.j)
        if (inky_coord == self.target):
            self.target = random_open_cell(self.maze)
        return (self.target)
