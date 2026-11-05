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
        self.slide_state = Slide_State.NONE
        self.slide_last_s = mlx.timer

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
        if (mlx.timer - self.slide_last_s >= TICK_DELAY):
            next_i, next_j = self.destination
            next_x, next_y = self.maze.smaze[next_i][next_j]["coor"]

            vector = Vector(next_x - self.x, next_y - self.y)
            step = (TICK_DELAY * 48) / 1
            vector = vector.unit_vector() * step

            x, y = vector.apply((self.x, self.y))
            x, y = int(x), int(y)
            # if ((x < next_x + step and x > next_x - step) and
            #    (y < next_y + step and y > next_y - step)):
            if (abs(x - next_x) < step and abs(y - next_y) < step):
                print(f"Correction needed player will be at ({x}, {y})", end="")
                x, y = next_x, next_y
            self.x, self.y = x, y

            print(f"{prefix} actual = ({self.x}, {self.y}), target = ({next_x}, {next_y})")
            self.slide_last_s = mlx.timer

            # Check if the entity reached its destination
            if (next_x == self.x and next_y == self.y):
                self.i, self.j = next_i, next_j
                self.slide_state = Slide_State.NONE

    def set_destination(self, i: int, j: int) -> None:
        self.destination = (i, j)
        self.slide_state = Slide_State.SLIDING
