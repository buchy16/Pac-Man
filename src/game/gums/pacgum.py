from .gum import Gum
from ..maze import Maze
from ..entities.player import Player


# i = height (y)
# j = width (x)

class Pacgum(Gum):
    """Regular pacgum collectible that only awards points."""

    def __init__(self, maze: Maze, i: int, j: int, pts: int) -> None:
        """Initialize a regular pacgum.

        Parameters
        ----------
        maze : Maze
            The maze containing the pacgum.
        i : int
            Row index of the pacgum in the maze matrix.
        j : int
            Column index of the pacgum in the maze matrix.
        pts : int
            Points awarded when the pacgum is eaten.
        """
        super().__init__(maze)
        self.i = i
        self.j = j
        self.x, self.y = self.maze.smaze[i][j]['coor']

        self.width = 0
        self.height = 0

        self.points = pts

    def eaten(self, player: Player) -> None:
        """Add the pacgum points to the player score.

        Parameters
        ----------
        player : Player
            The player who ate the pacgum.
        """
        player.score += self.points
