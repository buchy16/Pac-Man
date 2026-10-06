from .gum import Gum
from ..maze import Maze
from ..entities import Player


# i = height (y)
# j = width (x)

class SuperPacgum(Gum):
    """Special pacgum collectible that awards points and power state."""

    def __init__(self, maze: Maze, i: int, j: int, pts: int) -> None:
        """Initialize a super pacgum.

        Parameters
        ----------
        maze : Maze
            The maze containing the super pacgum.
        i : int
            Row index of the super pacgum in the maze matrix.
        j : int
            Column index of the super pacgum in the maze matrix.
        pts : int
            Points awarded when the super pacgum is eaten.
        """
        super().__init__(maze)
        self.i = i
        self.j = j
        self.x, self.y = self.maze.smaze[i][j]['coor']

        self.width = 0
        self.height = 0

        self.points = pts

    def eaten(self, player: Player) -> None:
        """Add the super pacgum points and activate the power-up.

        Parameters
        ----------
        player : Player
            The player who ate the super pacgum.
        """
        player.score += self.points
        player.super_pacgum = True
