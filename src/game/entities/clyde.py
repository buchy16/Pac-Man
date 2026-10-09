from ...directions import Direction
from .ghost import Ghost
from .player import Player
from ..maze import Maze
from ...utils import manhattan_dist, random_open_cell


"""Clyde se balade aléatoirement... et fonce sur Pacman quand il est proche"""


class Clyde(Ghost):
    MAGNETIC_DISTANCE: int = 8

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(maze, player, prefix, speed,
                         i_start, j_start, dir_start)

        self.width, self.height = 26, 26
        self.target = (0, 0)

    def get_target(self) -> tuple[int, int]:
        """determines the ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        clyde_coord = (self.i, self.j)
        player_coord = (self.player.i, self.player.j)
        if manhattan_dist(clyde_coord, player_coord) < self.MAGNETIC_DISTANCE:
            self.target = player_coord
        elif (clyde_coord == self.target):
            self.target = random_open_cell(self.maze)
        return (self.target)
