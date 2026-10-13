from ...directions import Direction
from .ghost import Ghost
from .player import Player
from ..maze import Maze

"""
when CHASER
    Blinky targets Pacman
when FRIGHTENED
    ToDo
"""


class Blinky(Ghost):
    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(maze, player, prefix, speed,
                         i_start, j_start, dir_start)

        self.target = (self.player.i, self.player.j)
        self.is_frozen = True

    def get_chase_target(self) -> tuple[int, int]:
        """determines the CHASER ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        return (self.player.i, self.player.j)

    def get_flee_target(self) -> tuple[int, int]:
        """determines the FRIGHTENED ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        # ToDo
        return (self.i_start, self.j_start)  # temp
