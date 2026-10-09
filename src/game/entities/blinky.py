from ...directions import Direction
from .ghost import Ghost
from .player import Player
from ..maze import Maze


"""Blinky chasse Pacman"""


class Blinky(Ghost):
    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(maze, player, prefix, speed,
                         i_start, j_start, dir_start)

        self.width, self.height = 26, 26
        self.target = (self.player.i, self.player.j)

    def get_target(self) -> tuple[int, int]:
        """determines the ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        return (self.player.i, self.player.j)
