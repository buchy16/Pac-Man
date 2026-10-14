from ..Mlx import mlx
from . import Maze
from . import Player
from . import PacgumManager
from ..parse_config import GameConfig
from .entities import GhostManager
from ..menu.pause_menu import PausMenu
from ..state import State
from src.utils import display_nums
from src.sprites import MENU


class Game(State):
    def __init__(self, config: GameConfig) -> None:
        self.number = 0
        mlx.new_window(1280, 720, "main")
        self.middle_X = int(1280 / 2)
        self.middle_Y = int(720 / 2)

        self.config = config
        self.maze = Maze(
            size=(config.level[0].width, config.level[0].height),
            seed=config.seed
            )

        self.player = Player(self.maze)

        self.pacgums = PacgumManager(self.player, self.maze, 10, 50)

        self.ghosts = GhostManager(self.player, self.maze)

        self.pause_menu = PausMenu()
        mlx.add_key_hook_function(self.open_pause_menu, "main")

    def open_pause_menu(self, keynum: int) -> None:
        if (mlx.KEYNAME[keynum] == "Escape"):
            self.pause_menu.activate_pause()

    def unload(self) -> State:
        from ..menu.main_menu import MainMenu
        mlx.close_window("main")
        return (MainMenu(self.config))

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> int:
        if (self.pause_menu.pause is False):
            self.player.move()
            # self.pacgums.display_pacgums()
            self.pacgums.update()
            self.ghosts.update()
        else:
            self.pause_menu.update_mouse()
            return (self.pause_menu.exiting)
        return (0)

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw_HUD(self) -> None:
        pts_offset = display_nums(7, 7, "main", str(self.player.score))
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            MENU["PTS"],
            pts_offset,
            0
        )

    def draw(self) -> None:
        self.maze.draw_maze()

        self.pacgums.draw()

        self.player.draw()

        self.ghosts.draw()

        self.draw_HUD()

        if (self.pause_menu.pause is True):
            self.pause_menu.draw_paus_menu()
