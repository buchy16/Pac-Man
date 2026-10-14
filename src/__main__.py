import commentjson
from pydantic import ValidationError
from .Mlx import mlx
from .state import State
from .menu import MainMenu
# from .game import Game
from .parse_config import parse_validate_config, GameConfig
from .utils import print_red

# On est pas en RGB mais en BGR


class App():
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.state: State = MainMenu(self.config)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        if (self.state.update() == 1):
            self.state = self.state.unload()

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        self.state.draw()


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
