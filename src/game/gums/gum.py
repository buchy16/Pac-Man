from abc import ABC, abstractmethod
from ..maze import Maze
from ..entities import Player


class Gum(ABC):
    """Base class for collectible items placed on the maze.

    The class stores the maze reference and the common attributes shared by
    regular and super pacgums.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize a gum instance.

        Parameters
        ----------
        maze : Maze
            The maze that owns the gum and provides tile coordinates.
        """
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
        """Apply the effect of eating the gum.

        Parameters
        ----------
        player : Player
            The player consuming the gum.
        """
        pass
