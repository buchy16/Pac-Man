from ...directions import Direction
from .ghost import Ghost
from .player import Player
from ..maze import Maze
from ...directions import DIR_MOVES

"""
when CHASER
    Pinky is aiming to be MAGNETIC_DISTANCE squares ahead of Pacman
when FRIGHTENED
    Pinky moves to the corner furthest from Pac-Man
    This target is updated when it is reached,
    or if Pac-Man has entered the same quarter of the maze as the target
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
        return (self.get_ahead_magnetic_target(self.MAGNETIC_DISTANCE))
