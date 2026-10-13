from ...directions import Direction
from .ghost import Ghost
from .player import Player
from ..maze import Maze
from ...utils import manhattan_dist, random_open_cell

"""
when CHASER
    Clyde moves randomly and targets Pacman when it's within MAGNETIC_DISTANCE
when FRIGHTENED
    ToDo
"""


class Clyde(Ghost):
    MAGNETIC_DISTANCE: int = 8

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(maze, player, prefix, speed,
                         i_start, j_start, dir_start)

        self.target = (self.i_start, self.j_start)

    def get_chase_target(self) -> tuple[int, int]:
        """determines the CHASER ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        clyde_coord = (self.i, self.j)
        player_coord = (self.player.i, self.player.j)
        if manhattan_dist(clyde_coord, player_coord) < self.MAGNETIC_DISTANCE:
            self.target = player_coord
        elif (clyde_coord == self.target):
            self.target = random_open_cell(self.maze)
        return (self.target)

    def get_flee_target(self) -> tuple[int, int]:
        """determines the FRIGHTENED ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        # ToDo
        return (self.i_start, self.j_start)  # temp
