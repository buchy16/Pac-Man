from abc import ABC, abstractmethod
from ..maze import Maze
from ..entities import Player


class Gum(ABC):
    def __init__(self, maze: Maze):
        self.points: int

        self.i: int
        self.j: int

        self.x: int
        self.y: int

        self.width: int
        self.height: int

        self.maze = maze

        self.was_eaten = False

    @abstractmethod
    def eaten(self, player: Player) -> None:
        pass
