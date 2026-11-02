from .targets import (
    NearbyTarget, PacmanTarget, TrickyTarget, RandomOrChargeTarget,
    CornerTarget
)
from .ghost import Ghost
from .player import Player
from ..maze import Maze
from ...utils.directions import Direction


class Pinky(Ghost):
    """
    when CHASER
        Pinky is aiming to be MAGNETIC_DISTANCE squares ahead of Pacman
    when FRIGHTENED
        Pinky moves to the corner furthest from Pac-Man
        This target is updated when it is reached,
        or if Pac-Man has entered the same quarter of the maze as the target
    """
    MAGNETIC_DISTANCE: int = 2

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(
            maze, player, prefix, speed, i_start, j_start, dir_start,
            chase_strategy=NearbyTarget(dist=self.MAGNETIC_DISTANCE,
                                        behind=False),
            flee_strategy=CornerTarget()
        )


class Blinky(Ghost):
    """
    when CHASER
        Blinky targets Pacman
    when FRIGHTENED
        Blinky moves to the corner furthest from Pac-Man
        This target is updated when it is reached,
        or if Pac-Man has entered the same quarter of the maze as the target
    """

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(
            maze, player, prefix, speed, i_start, j_start, dir_start,
            chase_strategy=PacmanTarget(),
            flee_strategy=CornerTarget()
        )


class Inky(Ghost):
    """
    when CHASER
        Inky aims at the point symmetrical to Blinky relative to the cell
        MAGNETIC_DISTANCE squares ahead of Pac-Man
    when FRIGHTENED
        Inky moves to the corner furthest from Pac-Man
        This target is updated when it is reached,
        or if Pac-Man has entered the same quarter of the maze as the target
    """
    MAGNETIC_DISTANCE: int = 2

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        # kept in an attribute: the very same object is used as
        # chase_strategy, so giving it Blinky later is enough
        self.tricky_target = TrickyTarget(dist=self.MAGNETIC_DISTANCE)

        super().__init__(
            maze, player, prefix, speed, i_start, j_start, dir_start,
            chase_strategy=self.tricky_target,
            flee_strategy=CornerTarget()
        )

        # will need blinky's position to calculate his target
        self.blinky_ptr: Ghost | None = None

    def set_blinky_ptr(self, blinky: Ghost) -> None:
        """Dependency injection: gives Inky access to Blinky"""
        self.blinky_ptr = blinky
        self.tricky_target.blinky = blinky


class Clyde(Ghost):
    """
    when CHASER
        Clyde moves randomly
        and targets Pacman at FAST_SPEED when it's within MAGNETIC_DISTANCE
    when FRIGHTENED
        Clyde moves to the corner furthest from Pac-Man
        This target is updated when it is reached,
        or if Pac-Man has entered the same quarter of the maze as the target
    """
    MAGNETIC_DISTANCE: int = 6

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        super().__init__(
            maze, player, prefix, speed, i_start, j_start, dir_start,
            chase_strategy=RandomOrChargeTarget(dist=self.MAGNETIC_DISTANCE),
            flee_strategy=CornerTarget()
        )
