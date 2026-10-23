from ..Mlx import mlx
from . import Maze
from . import Player
from . import PacgumManager
from ..data.parse_config import GameConfig
from .entities import GhostManager
from ..menu.pause_menu import PausMenu
from ..state import State
from ..utils.utils import display_nums
from ..utils.sprites import MENU, HUD, BACKGROUNDS


class Game(State):
    def __init__(self, config: GameConfig) -> None:
        self.level = 0
        mlx.new_window(1280, 720, "main")
        self.middle_X = int(1280 / 2)
        self.middle_Y = int(720 / 2)

        self.config = config
        self.maze = Maze(
            size=(config.level[0].width, config.level[0].height),
            seed=config.seed
            )

        self.timer = float(config.level_max_time)
        self.last_second = mlx.timer

        self.player = Player(self.maze)

        self.pacgums = PacgumManager(self.player, self.maze, 10, 50)

        self.ghosts = GhostManager(self.player, self.maze)

        self.game_ended = False

        self.pause_menu = PausMenu()
        mlx.add_key_hook_function(self.open_pause_menu, "main")

    def open_pause_menu(self, keynum: int) -> None:
        if (mlx.KEYNAME[keynum] == "Escape" and self.game_ended is False):
            self.pause_menu.activate_pause()

    def unload(self) -> State:
        from ..menu.main_menu import MainMenu
        mlx.close_window("main")
        return (MainMenu(self.config))

    def regenerate_maze(self) -> None:
        level = self.level
        self.maze = Maze(
            size=(self.config.level[level].width,
                  self.config.level[level].height),
            seed=self.config.seed
        )

    def next_level(self) -> None:
        self.level += 1
        self.regenerate_maze()

        # C'est pas très beau et très opti de tout recrer
        self.player = Player(self.maze)
        self.ghosts = GhostManager(self.player, self.maze)
        # on pourrait ajouter une methode dans entity qui actualise le maze
        # puis réinitialiser nos entitées exemple :
        #   self.ghosts.set_maze(self.maze)
        #   self.ghosts._reset_all_ghosts()
        #   self.player.reset()
        #   self.player.set_maze(self.maze)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def is_game_ended(self) -> bool:
        if (self.timer < 0 or self.player.life <= 0):
            self.game_ended = True
            return (True)
        return (False)

    def update(self) -> int:
        # if the timer as finished or pacman is dead,
        # we wait 2s befor sending 1 to return to the main menu
        if (self.is_game_ended()):
            if (mlx.timer - self.last_second >= 2.0):
                return (1)
            return (0)

        if (self.pause_menu.pause is False):
            self.player.move()
            # self.pacgums.display_pacgums()
            self.pacgums.update()
            self.ghosts.update()

            if (mlx.timer - self.last_second >= 1.0):
                self.timer -= 1
                self.last_second = mlx.timer
        else:
            self.pause_menu.update_mouse()
            return (self.pause_menu.exiting)
        return (0)

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw_game_over(self) -> None:
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            BACKGROUNDS["Game over"],
            0,
            0
        )

    def draw_pacman_lives(self, x: float, y: float) -> None:
        if (self.player.life <= 0):
            return
        LIVE_W = 20
        LIVE_H = 22

        for k in range(0, self.player.life):
            x_offset = (LIVE_W + 5) * k

            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                HUD["Lives"],
                int(x - (LIVE_W / 2) + x_offset),
                int(y - (LIVE_H / 2))
            )

    def draw_HUD(self) -> None:
        pts_offset = display_nums(10, 10, "main", str(self.player.score))
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            MENU["PTS"],
            pts_offset,
            0
        )

        # 39 = pts_y + 10 + pcaman lives icon height
        self.draw_pacman_lives(10, 39)

        # 55 = pcaman lives icon y + pcaman lives icon height / 2 + 5
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main"],
            0,
            55,
            0x7FCB36,
            f"Level {self.config.level[self.level].id}"
        )
        # 78 = I tried my best :c
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main"],
            0,
            78,
            0x0000FF,
            f"time left: {int(self.timer)}"
        )

    def draw(self) -> None:
        if (self.game_ended is False):
            self.maze.draw_maze()
            self.pacgums.draw()
            self.player.draw()
            self.ghosts.draw()
            self.draw_HUD()

            if (self.pause_menu.pause is True):
                self.pause_menu.draw_paus_menu()
        else:
            self.draw_game_over()
