from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ...utils.utils import manhattan_dist, not_closed_cell, random_open_cell
from ...utils.directions import DIR_MOVES

if TYPE_CHECKING:
    # only imported for type checking: avoids the circular import
    from .ghost import Ghost


# ================================================================= INTERFACE
class TargetStrategy(ABC):
    @abstractmethod
    def get_target(self, ghost: 'Ghost') -> tuple[int, int]:
        pass


# ---------------------------------------------------------- strategy: RANDOM
class RandomTarget(TargetStrategy):
    def get_target(self, ghost: 'Ghost') -> tuple[int, int]:
        """
        Returns : the coordinates (i, j) of a new random target
            once the previous target has been hit
        """
        current_coord = (ghost.i, ghost.j)
        if (current_coord == ghost.target):
            return (random_open_cell(ghost.maze))
        return (ghost.target)


# ---------------------------------------------------------- strategy: PACMAN
class PacmanTarget(TargetStrategy):
    def get_target(self, ghost: 'Ghost') -> tuple[int, int]:
        """
        Returns : the coordinates (i, j) of pacman
        """
        return (ghost.player.i, ghost.player.j)


# ---------------------------------------------------------- strategy: CORNER
class CornerTarget(TargetStrategy):
    def get_target(self, ghost: 'Ghost') -> tuple[int, int]:
        """
        Returns : the coordinates (i, j) of the ghost corner
        """
        return ((ghost.i_corner, ghost.j_corner))


# --------------------------------------------------- strategy: NEARBY PACMAN
class NearbyTarget(TargetStrategy):
    def __init__(self, dist: int, behind: bool = False) -> None:
        # specific configuration for this strategy
        self.dist = dist
        self.behind = behind

    def get_target(self, ghost: 'Ghost') -> tuple[int, int]:
        """Returns: the coordinates (i, j) of the further valid cell
            from `dist` to 0 squares ahead/behind player"""
        direction = ghost.player.direction
        if self.behind:
            direction = direction.opposite
        di, dj = DIR_MOVES.get(direction, (0, 0))

        max_row = ghost.maze._height - 1
        max_col = ghost.maze._width - 1

        # checks the cells from `dist` to 0 squares ahead/behind the player
        for steps in range(self.dist, -1, -1):
            target_row = min(max(ghost.player.i + di * steps, 0), max_row)
            target_col = min(max(ghost.player.j + dj * steps, 0), max_col)

            if not_closed_cell(ghost.maze, target_row, target_col):
                return (target_row, target_col)

        # when direction==NONE, `DIR_MOVES.get()` returns player's position...
        # => belt, suspenders and mypy :D
        return (ghost.player.i, ghost.player.j)


# ----------------------------------------------- strategy: RANDOM AND CHARGE
class RandomOrChargeTarget(TargetStrategy):
    def __init__(self, dist: int) -> None:
        # specific configuration for this strategy
        self.dist = dist

    def get_target(self, ghost: 'Ghost') -> tuple[int, int]:
        """
        Returns: the coordinates (i, j) of a new random target
            once the previous target has been hit
            tuple[int, int]: moves around at random
                            and charges at Pac-Man when he is close
        """
        current_coord = (ghost.i, ghost.j)
        player_coord = (ghost.player.i, ghost.player.j)
        if manhattan_dist(current_coord, player_coord) < self.dist:
            ghost.speed = ghost.FAST_SPEED
            return (player_coord)
        elif (current_coord == ghost.target):
            ghost.speed = ghost.normal_speed
            return (random_open_cell(ghost.maze))
        ghost.speed = ghost.normal_speed
        return (ghost.target)


# ------------------------------------------------------- strategy: TRICKY
class TrickyTarget(TargetStrategy):
    def __init__(self, dist: int, blinky: 'Ghost | None' = None) -> None:
        # specific configuration for this strategy
        self.dist = dist
        # provided later by the GhostManager (see Inky.set_blinky_ptr)
        self.blinky = blinky

    def get_target(self, ghost: 'Ghost') -> tuple[int, int]:
        """
        Computes a point such that the middle between this point and Blinky
        is the cell located `dist` squares ahead of Pac-Man.
        The point is clamped to the maze. If it is a closed cell, we go
        back towards the ghost until a valid cell is found.

        Returns:
        the coordinates (i, j) of the furthest valid cell
        on the way from the ghost to the point
        """

        # in case the manager has not provided the reference to Blinky
        if self.blinky is None:
            return (ghost.player.i, ghost.player.j)

        di, dj = DIR_MOVES.get(ghost.player.direction, (0, 0))
        ahead_i = ghost.player.i + self.dist * di
        ahead_j = ghost.player.j + self.dist * dj

        # point symmetrical to Blinky relative to the cell ahead of Pac-Man
        temp_i = 2 * ahead_i - self.blinky.i
        temp_j = 2 * ahead_j - self.blinky.j
        max_row = ghost.maze._height - 1
        max_col = ghost.maze._width - 1
        inside_i = min(max(temp_i, 0), max_row)
        inside_j = min(max(temp_j, 0), max_col)

        # offset from the ghost to the point, shortened one step at a time
        # (along the longest axis) until a valid cell is found
        off_i = inside_i - ghost.i
        off_j = inside_j - ghost.j
        while off_i != 0 or off_j != 0:
            target_row = ghost.i + off_i
            target_col = ghost.j + off_j
            if not_closed_cell(ghost.maze, target_row, target_col):
                return (target_row, target_col)

            if abs(off_i) >= abs(off_j):
                off_i -= (off_i > 0) - (off_i < 0)
            else:
                off_j -= (off_j > 0) - (off_j < 0)

        # belt, suspenders and mypy :D
        return (ghost.player.i, ghost.player.j)
