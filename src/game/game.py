from ..Mlx import mlx
from .maze import Maze
from .entities.player import Player
from .gums.pacgum_manager import PacgumManager
from ..data.parse_config import GameConfig
from ..data.scores import HighScoreStorage
from .entities.ghost_manager import GhostManager
from .cheats.cheat import Cheat
from .end_screen import EndScreen
from .hud import Hud
from ..menu.pause_menu import PausMenu
from ..state import State
from ..utils.sprites import BACKGROUNDS


PTS_LENGHT = 34


class Game(State):
    """Manage the main Pac-Man game state."""

    def __init__(self, config: GameConfig,
                 hight_score: HighScoreStorage) -> None:
        """Initialize a game with its configuration and score storage.

        Args:
            config: Configuration used to set up the game.
            hight_score: Storage for the player's high score.
        """
        self.level = 0
        self.last_level = len(config.level) - 1

        mlx.new_window(1280, 720, "main")
        self.middle_X = int(1280 / 2)
        self.middle_Y = int(720 / 2)

        self.config = config
        self.hight_score = hight_score
        self.maze = Maze(
            size=(config.level[0].width, config.level[0].height),
            seed=config.seed
            )

        self.timer = float(config.level_max_time)
        self.last_second = mlx.timer

        self.player = Player(self.maze)

        self.hud = Hud(self.player, self.config.level[self.level].id)

        self.pacgums = PacgumManager(self.player, self.maze,
                                     config.points_per_pacgum,
                                     config.points_per_super_pacgum)

        self.ghosts = GhostManager(self.player,
                                   self.maze,
                                   config.points_per_ghost)

        self.cheat_mod = Cheat(self.player, self.ghosts, self.pacgums)

        self.game_ended = False

        self.end_screen = EndScreen(self.hight_score, self.player)

        self.pause_menu = PausMenu()
        mlx.add_key_hook_function(self.open_pause_menu, "main")
        mlx.add_key_hook_function(self.enable_disable_cheat, "main")

    def open_pause_menu(self, keynum: int) -> None:
        """Open the pause menu when the Escape key is pressed.

        Args:
            keynum: Numeric identifier of the pressed key.
        """
        if (mlx.KEYNAME[keynum] == "Escape" and self.game_ended is False):
            self.pause_menu.activate_pause()

    def enable_disable_cheat(self, keynum: int) -> None:
        """Toggle cheat mode when the F3 key is pressed.

        Args:
            keynum: Numeric identifier of the pressed key.
        """
        if (mlx.KEYNAME[keynum] == "F3"):
            self.cheat_mod.enable_disable()

    def unload(self) -> State:
        """Close the game window and return to the main menu."""
        from ..menu.main_menu import MainMenu
        mlx.close_window("main")
        return (MainMenu(self.config, self.hight_score))

    def next_level(self) -> None:
        """Advance to the next level and reset level-specific game objects."""
        self.level += 1
        if (self.level > self.last_level):
            return

        self.timer = float(self.config.level_max_time)
        self.maze.regenerate_maze(
            size=(self.config.level[self.level].width,
                  self.config.level[self.level].height),
            seed=self.config.seed)

        self.ghosts._reset_all_ghosts()
        self.player.reset()

        self.pacgums = PacgumManager(self.player, self.maze,
                                     self.config.points_per_pacgum,
                                     self.config.points_per_super_pacgum)
        self.cheat_mod.set_new_pacgums(self.pacgums)

        self.hud.set_level(self.config.level[self.level].id)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def is_game_ended(self) -> bool:
        """Return whether the player has lost all lives or time has expired."""
        if (self.timer < 0 or self.player.life <= 0):
            self.game_ended = True
            return (True)
        return (False)

    def update(self) -> int:
        """Update the game state and return its transition status.

        Returns:
            The end-screen or pause-menu status, or 0 while the game
            continues normally.
        """
        # if the timer as finished or pacman is dead or all level are passed,
        if (self.is_game_ended() or self.level > self.last_level):
            if (self.end_screen.enable is False):
                # destroy all bake_background to free memory
                self.maze.destroy_background()
                self.pacgums.destroy_img()
                self.hud.destroy_img()

                self.end_screen.enable_disable()

                if (self.cheat_mod.enable is True):
                    self.cheat_mod.enable_disable()

            return (self.end_screen.update())

        if (self.pause_menu.pause is False):
            self.player.move()
            self.pacgums.update()
            self.ghosts.update()
            self.cheat_mod.update()
            self.hud.update()

            if (self.pacgums.all_gums_eaten() is True):
                self.next_level()

            if (self.cheat_mod.timer_frozen is False and
               mlx.timer - self.last_second >= 1.0):
                self.timer -= 1
                self.last_second = mlx.timer
        else:
            self.pause_menu.update_mouse()
            return (self.pause_menu.exiting)
        return (0)

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        """Draw the current game screen and active game elements."""
        if (self.game_ended is True):
            self.end_screen.draw(BACKGROUNDS["Game over"])
        elif (self.level > self.last_level):
            self.end_screen.draw(BACKGROUNDS["You won"])
        else:
            self.maze.draw_maze()
            self.pacgums.draw()
            self.player.draw()
            self.ghosts.draw()
            self.hud.draw(self.timer)

            self.cheat_mod.draw()

            if (self.pause_menu.pause is True):
                self.pause_menu.draw_paus_menu()
