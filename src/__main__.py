import sys
import logging
from .Mlx import mlx
from .menu import MainMenu
from .parse_config import get_valid_config, GameConfig
from .game import Game

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# On est pas en RGB mais en BGR


class App():
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.main_menu = MainMenu(self.config)
        self.game: Game | None = None

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        if (self.main_menu.game_started is True):
            if (self.game is None):
                self.game = Game((self.config.level[0].width,
                                  self.config.level[0].height))
            else:
                self.game.update()
        else:
            self.main_menu.update()

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        if (self.main_menu.game_started is True):
            self.game.draw()
        else:
            self.main_menu.draw()


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


if __name__ == "__main__":
    main(sys.argv)
