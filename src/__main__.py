import commentjson
from .Mlx import mlx
from .menu import MainMenu
from .parse_config import parse_validate_config, GameConfig
from .game import Game
from .utils import print_red
from pydantic import ValidationError

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
    print("begining tests")
    try:
        config = parse_validate_config("config.json")
    except FileNotFoundError as err:
        print_red(f"Config file is missing : {err}")
        return
    except commentjson.JSONLibraryException as e:
        err = str(e).split("Traceback")[0].strip()
        print_red(f"Config file has invalid syntax :\n{err}")
        return
    except ValidationError as err:
        print_red(f"Config validation error : {err.errors()[0]['msg']}")
        return

    pac_man = App(config)

    mlx.run(pac_man.update, pac_man.draw)


if __name__ == "__main__":
    main()
