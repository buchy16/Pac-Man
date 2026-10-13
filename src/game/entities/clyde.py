from ...directions import Direction
from .ghost import Ghost
from .player import Player
from ..maze import Maze
from ...utils import manhattan_dist, random_open_cell

# from math import ceil

"""
when CHASER
    Clyde moves randomly
    and targets Pacman at ROCKET_SPEED when it's within MAGNETIC_DISTANCE
when FRIGHTENED
    Clyde moves to the corner furthest from Pac-Man
    This target is updated when it is reached,
    or if Pac-Man has entered the same quarter of the maze as the target
"""


class Clyde(Ghost):
    MAGNETIC_DISTANCE: int = 8

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(maze, player, prefix, speed,
                         i_start, j_start, dir_start)

        self.target = random_open_cell(self.maze)

    def get_chase_target(self) -> tuple[int, int]:
        """determines the CHASER ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        clyde_coord = (self.i, self.j)
        player_coord = (self.player.i, self.player.j)
        if manhattan_dist(clyde_coord, player_coord) < self.MAGNETIC_DISTANCE:
            self.speed = self.ROCKET_SPEED  # 0.75 
            return (player_coord)
        elif (clyde_coord == self.target):
            self.speed = self.normal_speed
            return (random_open_cell(self.maze))
        self.speed = self.normal_speed
        return (self.target)

    # def get_flee_target(self) -> tuple[int, int]:
    #     """determines the FRIGHTENED ghost's target on the grid
    #     Returns : the coordinates (i, j) of the cell to target
    #     """
    #     player_coord = (self.player.i, self.player.j)
    #     center_coord = (ceil(self.maze._width / 2) - 1,
    #                     ceil(self.maze._height / 2) - 1)
    #     player_to_target = manhattan_dist(player_coord, self.target)
    #     center_to_target = manhattan_dist(center_coord, self.target)
    #     # s'il a atteint sa target
    #     if ((self.i, self.j == self.target)
    #         # ou si Pacman est rentré dans le même quart que la cible
    #         or player_to_target < center_to_target):
    #         # print(f"DEBUG\tCLYDE target:\t{self.target}")
    #         # print(f"DEBUG\tPLAYER coord:\t{player_coord}")
    #         self.target = self.get_furthest_corner()
    #         # print(f"DEBUG\tCLYDE new frightened TARGET:\t{self.target}")
    #     return (self.target)
