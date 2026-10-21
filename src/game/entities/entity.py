from abc import ABC, abstractmethod
from ..maze import Maze
from ...utils.directions import Direction


class Entity(ABC):
    """Base class for entities placed on the maze.

    The class stores the maze reference
    and the common attributes shared by Pacman and ghosts.
    """
    ENTITY_SIZE: int = 26

    def __init__(self, maze: Maze) -> None:
        """Initialize an entity (player / ghost) instance.

        Parameters
        ----------
        maze : Maze
            The maze that owns the gum and provides tile coordinates.
        """
        self.life: int  # /!\ inutile pour ghosts depuis ajout GhostState=DEAD

        self.maze = maze
        self.width: int = self.ENTITY_SIZE
        self.height: int = self.ENTITY_SIZE

        # position in pixels
        self.x: int
        self.y: int

        # position in grid
        self.i: int
        self.j: int
        # initial position
        self.i_start: int
        self.j_start: int

        self.direction: Direction

    @abstractmethod
    def move(self) -> None:
        """If the desired time has elapsed since the last movement,
        moves the entity by grid coordinates (i,j) and pixel coordinates (x,y)
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """animates the entity by alternating between several sprites
        corresponding to the direction in which it is moving.
        """
        pass
