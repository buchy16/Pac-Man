from abc import ABC, abstractmethod
from enum import Enum, auto
from ..maze import Maze
from ...utils.directions import Direction
from ...Mlx import mlx
from ...utils.utils import manhattan_dist


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
    ENTITY_COLLISION_MARGIN = 4

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

        # smooth slide
        self.destination: tuple[int, int]
        self.start_pos: tuple[int, int]
        self.time_start: float
        self.dist: int
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

    def slide(self) -> None:
        """establishes the player’s coordinates, over a given distance,
        in proportion to the time elapsed since the start of the movement
        Example: if I have 48 pixels to scan and speed = 1s, then in 1s
        I must have traveled 48 pixels
        """
        pp: float  # pp for Progress_Percentage
        dest_i, dest_j = self.destination
        dest_x, dest_y = self.maze.smaze[dest_i][dest_j]['coor']

        # 48 is the size of a cell
        # if speed = 1s and dist = 48 then slide_duration = 1s
        # but if dist = 24 then slide_duration = 0.5s (we have 2x less pixels
        # to be traveled at the same speed, 48px every 1)
        slide_duration = self.speed * (self.dist / 48)
        if slide_duration > 0:
            # percentage of current time compared to the given duration for
            # cover the distance
            pp = min((mlx.timer - self.time_start) / slide_duration, 1.0)
        else:
            pp = 1.0

        # we apply the pp by multiplying the distance between origin and
        # arrival by the pp to obtain a portion proportional to the time it
        # we are left to cover our distance
        self.x = round(self.start_pos[0] + ((dest_x - self.start_pos[0]) * pp))
        self.y = round(self.start_pos[1] + ((dest_y - self.start_pos[1]) * pp))

        # we have reached the allotted time
        if (pp >= 1.0):
            self.x = dest_x
            self.y = dest_y
            self.i, self.j = dest_i, dest_j
            self.slide_state = Slide_State.NONE

    def set_destination(self, i: int, j: int) -> None:
        """Set all parameters for a sliding effect to cell i, j

        Args:
            i (int): row
            j (int): column
        """
        self.destination = (i, j)
        self.start_pos = (self.x, self.y)
        self.slide_state = Slide_State.SLIDING

        dest_x, dest_y = self.maze.smaze[i][j]['coor']
        self.dist = manhattan_dist((dest_x, dest_y), (self.x, self.y))

        self.time_start = mlx.timer

    def reset_sliding(self) -> None:
        """Reset slide effect
        """
        self.slide_state = Slide_State.NONE
