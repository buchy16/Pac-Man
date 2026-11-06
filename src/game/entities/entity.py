from abc import ABC, abstractmethod
from enum import Enum, auto
from ..maze import Maze
from ...utils.directions import Direction
from ...utils.Vector import Vector
from ...Mlx import mlx


class Slide_State(Enum):
    SLIDING = auto()
    NONE = auto()


TICK_DELAY = 0.1


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

        self.destination: tuple[int, int]
        self.start_pos: tuple[int, int]
        self.time_start: float | None = None
        self.slide_state = Slide_State.NONE

        self.speed = 1.0

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

    def slide(self, prefix: str) -> None:
        dest_x, dest_y = self.maze.smaze[self.destination[0]][self.destination[1]]['coor']
        pp = min((mlx.timer - self.time_start) / self.speed, 1.0)

        self.x = round(self.start_pos[0] + ((dest_x - self.start_pos[0]) * pp))
        self.y = round(self.start_pos[1] + ((dest_y - self.start_pos[1]) * pp))

        if (pp >= 1.0):
            self.x = dest_x
            self.y = dest_y
            self.i, self.j = self.destination
            self.slide_state = Slide_State.NONE
            self.time_start = mlx.timer

        # print(f"{prefix}: current = ({self.x}, {self.y}), target = ({dest_x}, {dest_y}), p = {pp}")

    def set_destination(self, i: int, j: int) -> None:
        self.destination = (i, j)
        self.start_pos = (self.x, self.y)
        self.slide_state = Slide_State.SLIDING

        if (self.time_start is None):
            self.time_start = mlx.timer

    def reset_sliding(self) -> None:
        self.slide_state = Slide_State.NONE
        self.time_start = None
