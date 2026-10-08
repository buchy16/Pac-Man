from ..Mlx import mlx
from . import Maze
from . import Player
from . import PacgumManager
from ..directions import Direction
from .entities import Blinky, Clyde, Inky, Pinky


class Game():
    def __init__(self, size: tuple[int, int] = (15, 15), seed=42) -> None:
        self.number = 0
        mlx.new_window(1280, 720, "main")
        self.middle_X = int(1280 / 2)
        self.middle_Y = int(720 / 2)

        self.maze = Maze(size=size, seed=seed)

        self.player = Player(self.maze)

        self.pacgums = PacgumManager(self.player, self.maze, 10, 50)

        self.blinky = Blinky(self.maze, self.player, "b", 0, 0, Direction.EAST)
        self.clyde = Clyde(self.maze, self.player, "c", 0, 14, Direction.SOUTH)
        self.inky = Inky(self.maze, self.player, "i", 14, 14, Direction.WEST)
        self.pinky = Pinky(self.maze, self.player, "p", 14, 0, Direction.NORTH)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        self.player.move()
        # self.pacgums.display_pacgums()

        self.pacgums.update()

        self.blinky.move()
        self.clyde.move()
        self.inky.move()
        self.pinky.move()

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        self.maze.draw_maze()

        self.pacgums.draw()

        self.player.draw()

        self.blinky.draw()
        self.clyde.draw()
        self.inky.draw()
        self.pinky.draw()

        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main"],
            0,
            0,
            0x0000FFFF,
            str(self.player.score)
        )

        # self.maze.display_Smaze()
