from .Mlx import mlx
from .menu import MainMenu
from .parse_config import parsing
from .game import Game

# On est pas en RGB mais en BGR


class App():
    def __init__(self) -> None:
        self.main_menu = MainMenu()
        self.game: Game | None = None

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        if (self.main_menu.game_started is True):
            if (self.game is None):
                self.game = Game((15, 8))
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


def main():
    parsing("config.json")
    print("begining tests")
    pac_man = App()

    mlx.run(pac_man.update, pac_man.draw)


if __name__ == "__main__":
    main()
