import sys
import logging
from .Mlx import mlx
from .menu.main_menu import MainMenu
from .data.parse_config import get_valid_config, GameConfig
from .data.scores import HighScoreStorage
from .state import State
from .utils.utils import display_string, display_nums
from .utils.sprites import second_impact
from .utils.paths import resolve_path


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# On est pas en RGB mais en BGR


class App():
    """Coordinate the game configuration, state, update, and drawing."""

    def __init__(self, config: GameConfig) -> None:
        """Initialize the application with the game configuration.

        Args:
            config: Configuration used to initialize the game.
        """
        self.config = config
        self.scores = HighScoreStorage()
        self.state: State = MainMenu(self.config, self.scores)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        """Update the current state and load the next state when required."""
        if (self.state.update() == 1):
            self.state = self.state.unload()

# -----------------------------------------------------------------------------
# -------------------------------    DRAW   -----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        """Draw the current game state."""
        self.state.draw()


def main(argv: list[str]) -> None:
    """Run the Pac-Man application.

    Args:
        argv: Command-line arguments used to load the game configuration.
    """
    print("begining tests")
    if len(argv) != 2:
        spelling_fanatic = "argument" if len(argv) == 1 else "arguments"
        logging.error(f"You gave {len(argv) - 1} {spelling_fanatic}, "
                      "exactly 1 was required: TRY AGAIN")
        sys.exit(1)

    config = get_valid_config(str(resolve_path(argv[1])))

    pac_man = App(config)

    mlx.run(pac_man.update, pac_man.draw)

    display_string.unload_assets()
    display_nums.unload_assets()
    second_impact()


if __name__ == "__main__":
    main(sys.argv)
