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


PTS_LENGHT = 34


class Game(State):
    def __init__(self, config: GameConfig) -> None:
        self.level = 0
        self.last_level = len(config.level) - 1

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

        self.pacgums = PacgumManager(self.player, self.maze,
                                     config.points_per_pacgum,
                                     config.points_per_super_pacgum)

        self.ghosts = GhostManager(self.player, self.maze)

        self.game_ended = False

        self.pause_menu = PausMenu()
        mlx.add_key_hook_function(self.open_pause_menu, "main")
        mlx.add_key_hook_function(self.level_debug, "main")

        self.debug_eatall = False

    def open_pause_menu(self, keynum: int) -> None:
        if (mlx.KEYNAME[keynum] == "Escape" and self.game_ended is False):
            self.pause_menu.activate_pause()

    def unload(self) -> State:
        from ..menu.main_menu import MainMenu
        mlx.close_window("main")
        return (MainMenu(self.config))

    def next_level(self) -> None:
        self.level += 1
        if (self.level > self.last_level):
            return

        self.debug_eatall = False
        self.maze.regenerate_maze(
            size=(self.config.level[self.level].width,
                  self.config.level[self.level].height),
            seed=self.config.seed)
        # self.ghosts._reset_all_ghosts()
        # ^
        # |
        # |
        # Peut pas faire ça car le i_start et j_start  des phantomes
        # correspondent à l'ancien labyrithe après le changement de celui-ci
        self.ghosts = GhostManager(self.player, self.maze)  # <- temporaire

        self.player.reset()

        self.pacgums = PacgumManager(self.player, self.maze,
                                     self.config.points_per_pacgum,
                                     self.config.points_per_super_pacgum)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def is_game_ended(self) -> bool:
        if (self.timer < 0 or self.player.life <= 0):
            self.game_ended = True
            return (True)
        return (False)

    def update(self) -> int:
        # if the timer as finished or pacman is dead or all level are passed,
        # we wait 3s befor sending 1 to return to the main menu
        if (self.is_game_ended() or self.level > self.last_level):
            if (mlx.timer - self.last_second >= 3.0):
                return (1)
            return (0)

        if (self.pause_menu.pause is False):
            self.player.move()
            self.pacgums.update()
            self.ghosts.update()
            self.debug_eat()

            if (self.pacgums.all_gums_eaten() is True):
                self.next_level()

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
        score_lenght = len(str(self.player.score)) * 14 + PTS_LENGHT
        pts_offset = display_nums(
            640 - int((score_lenght / 2)) + 7,
            360,
            "main",
            str(self.player.score)
            )
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            MENU["PTS"],
            pts_offset,
            360 - 7
        )

    def draw_win(self) -> None:
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            BACKGROUNDS["You won"],
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
        if (self.game_ended is True):
            self.draw_game_over()
        elif (self.level > self.last_level):
            self.draw_win()
        else:
            self.maze.draw_maze()
            self.pacgums.draw()
            self.player.draw()
            self.ghosts.draw()
            self.draw_HUD()

            if (self.pause_menu.pause is True):
                self.pause_menu.draw_paus_menu()

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def level_debug(self, keynum: int) -> None:
        if (mlx.KEYNAME[keynum] == "n" and self.game_ended is False):
            self.debug_eatall = True
            for line in self.pacgums.pacgums:
                for gum in line:
                    if (gum.was_eaten is False):
                        gum.was_eaten = True
                        self.pacgums.update_img()
                        return

    def debug_eat(self) -> None:
        if (self.debug_eatall is True):
            for line in self.pacgums.pacgums:
                for gum in line:
                    if (gum.was_eaten is False):
                        gum.was_eaten = True
                        self.pacgums.update_img()
                        return
