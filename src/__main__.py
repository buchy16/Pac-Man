import sys
import logging
from .Mlx import mlx
from .menu import MainMenu
from .data.parse_config import get_valid_config, GameConfig
from .data.scores import HighScoreStorage
from .state import State
from .utils.utils import display_string, display_nums

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# On est pas en RGB mais en BGR


class App():
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.scores = HighScoreStorage()
        self.state: State = MainMenu(self.config, self.scores)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        if (self.state.update() == 1):
            self.state = self.state.unload()

# -----------------------------------------------------------------------------
# -------------------------------    DRAW   -----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        self.state.draw()


def main(argv: list) -> None:
    print("begining tests")
    if len(argv) != 2:
        spelling_fanatic = "argument" if len(argv) == 1 else "arguments"
        logging.error(f"You gave {len(argv) - 1} {spelling_fanatic}, "
                      "exactly 1 was required: TRY AGAIN")
        sys.exit(1)
    config = get_valid_config(argv[1])

    pac_man = App(config)

    mlx.run(pac_man.update, pac_man.draw)

    display_string.unload_assets()
    display_nums.unload_assets()


if __name__ == "__main__":
    main(sys.argv)
