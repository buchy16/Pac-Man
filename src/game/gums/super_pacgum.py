from .gum import Gum
from ..maze import Maze
from ..entities import Player


# i = height (y)
# j = width (x)

class SuperPacgum(Gum):
    def __init__(self, maze: Maze, i: int, j: int, pts: int) -> None:
        super().__init__(maze)
        self.i = i
        self.j = j
        self.x, self.y = self.maze.smaze[i][j]['coor']

        self.width = 0
        self.height = 0

        self.points = pts

    def eaten(self, player: Player):
        player.score += self.points
        player.super_pacgum = True
