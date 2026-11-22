from .targets import (
    NearbyTarget, PacmanTarget, TrickyTarget, RandomOrChargeTarget,
    FleeTarget
)
from .ghost import Ghost
from .player import Player
from ..maze import Maze
from ...utils.directions import Direction


"""
4 types of ghost
    Blinky targets directly Pac-Man
    Pinky targets 3 squares in front of Pac-Man
    Inky chases Pac-Man in a team with Blinky
    Clyde moves randomly and charges when Pac-Man is 3 squares or fewer away
"""


class Pinky(Ghost):
    """
    when CHASER
        Pinky is aiming to be MAGNETIC_DISTANCE squares ahead of Pacman
    when FRIGHTENED
        From the possible moves,
        choose the one that takes him furthest away from Pacman
    """
    MAGNETIC_DISTANCE: int = 3

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 corner_start: tuple[int, int], dir_start: Direction) -> None:
        super().__init__(
            maze, player, prefix, speed, corner_start, dir_start,
            chase_strategy=NearbyTarget(dist=self.MAGNETIC_DISTANCE,
                                        behind=False),
            flee_strategy=FleeTarget()
        )


class Blinky(Ghost):
    """
    when CHASER
        Blinky targets Pacman
    when FRIGHTENED
        From the possible moves,
        choose the one that takes him furthest away from Pacman
    """

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 corner_start: tuple[int, int], dir_start: Direction) -> None:
        super().__init__(
            maze, player, prefix, speed, corner_start, dir_start,
            chase_strategy=PacmanTarget(),
            flee_strategy=FleeTarget()
        )


class Inky(Ghost):
    """
    when CHASER
        Inky aims at the point symmetrical to Blinky relative to the cell
        MAGNETIC_DISTANCE squares ahead of Pac-Man
    when FRIGHTENED
        From the possible moves,
        choose the one that takes him furthest away from Pacman
    """
    MAGNETIC_DISTANCE: int = 2

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 corner_start: tuple[int, int], dir_start: Direction) -> None:
        # kept in an attribute: the very same object is used as
        # chase_strategy, so giving it Blinky later is enough
        self.tricky_target = TrickyTarget(dist=self.MAGNETIC_DISTANCE)

        super().__init__(
            maze, player, prefix, speed, corner_start, dir_start,
            chase_strategy=self.tricky_target,
            flee_strategy=FleeTarget()
        )

    def set_blinky_ptr(self, blinky: Ghost) -> None:
        """Dependency injection: gives Inky access to Blinky"""
        self.tricky_target.blinky = blinky


class Clyde(Ghost):
    """
    when CHASER
        Clyde moves randomly
        and targets Pacman at FAST_SPEED when it's within MAGNETIC_DISTANCE
    when FRIGHTENED
        From the possible moves,
        choose the one that takes him furthest away from Pacman
    """
    MAGNETIC_DISTANCE: int = 3

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 corner_start: tuple[int, int], dir_start: Direction) -> None:
        super().__init__(
            maze, player, prefix, speed, corner_start, dir_start,
            chase_strategy=RandomOrChargeTarget(dist=self.MAGNETIC_DISTANCE),
            flee_strategy=FleeTarget()
        )
