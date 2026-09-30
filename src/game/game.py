from ..Mlx import mlx
from . import Maze
from . import Player


class Game():
    def __init__(self, size: tuple[int, int] = (15, 15), seed=42) -> None:
        self.number = 0
        mlx.new_window(1280, 720, "main")
        self.middle_X = int(1280 / 2)
        self.middle_Y = int(720 / 2)

        self.maze = Maze(size=size, seed=seed)

        self.player = Player(self.maze)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        self.player.move()

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        self.maze.draw_maze()

        self.player.draw()

        # self.maze.display_Smaze()
