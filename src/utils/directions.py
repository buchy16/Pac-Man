"""Define movement directions and their corresponding grid vectors."""

from enum import IntFlag, auto


class Direction(IntFlag):
    """Represent a cardinal movement direction as a bit flag."""

    NONE = 0         # 0b0000 (0 = pas de direction)
    NORTH = auto()   # 0b0001 (1)
    EAST = auto()    # 0b0010 (2)
    SOUTH = auto()   # 0b0100 (4)
    WEST = auto()    # 0b1000 (8)

    # Does NOT handle flag COMBINATIONS: only call on simple directions
    @property
    def opposite(self) -> "Direction":
        """Return the opposite of the current direction."""
        opposites = {
            Direction.NONE: Direction.NONE,
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[self]

    # Does NOT handle flag COMBINATIONS: only call on simple directions
    @property
    def label(self) -> str:
        """Return the lowercase name of the current direction."""
        assert self.name is not None  # to silence MyPy
        return self.name.lower()


# moving vectors: (delta_row, delta_col)
DIR_MOVES = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
}
