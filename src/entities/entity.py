from abc import ABC, abstractmethod
from ..maze import Maze


class Entity(ABC):
    def __init__(self, maze: Maze) -> None:
        self.life: int
        self.x: int
        self.y: int
        self.maze = maze

    @abstractmethod
    def move(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
