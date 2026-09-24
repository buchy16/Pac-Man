from . import Entity
from ..maze import Maze


class Player(Entity):
    def __init__(self, maze: Maze, life: int = 3) -> None:
        super().__init__(maze)
        self.life = life

        xy = maze.smaze[maze._width // 2][maze._height // 2]["coor"]
        self.x, self.y = xy
