from src.Mlx import mlx
from src.game.entities.player import Player
from src.game.entities.ghost_manager import GhostManager
from src.utils.utils import SPECIAL_CHAR


class Cheat():
    def __init__(self, player: Player, ghosts: GhostManager):
        self.player = player
        self.ghosts = ghosts

        self.enable = False

        self.buffer = ""
        self.last_command = ""

    def enable_disable(self) -> None:
        if (self.enable is False):
            mlx.add_key_hook_function(
                self.listen_keyboard,
                "main"
            )
            self.enable = True
            print("cheat activated")
        else:
            mlx.rm_key_hook_function(
                self.listen_keyboard,
                "main"
            )
            print("cheat deactivated")
            self.enable = False

    def listen_keyboard(self, keynum: int) -> None:
        # print(f"[{mlx.KEYNAME[keynum]}]")
        key = mlx.KEYNAME[keynum]

        if (key == "BackSpace"):
            self.buffer = self.buffer[:-1]
        elif (key == "Return"):
            self.command_analyser()
        elif (key == "Tab"):
            self.buffer = self.last_command
        elif (len(key) == 1):
            if ((ord(key) >= 97 and ord(key) <= 122) or
               (ord(key) >= 48 and ord(key) <= 57)):
                self.buffer += key
        elif (key in SPECIAL_CHAR.keys()):
            self.buffer += SPECIAL_CHAR[key]

    def command_analyser(self) -> None:
        if (len(self.buffer) <= 0):
            return

        raw_command = self.buffer.split(" ")
        command = raw_command[0]
        if (len(raw_command) > 1):
            args = raw_command[1:]

        if (command == "kill"):
            self.player.life = 0
        elif (command == "reset-all"):
            self.ghosts._reset_all_ghosts()
        elif (command == "set-life"):
            self.set_player_life(args)
        else:
            print("Unkow commande")
            self.buffer = ""
            return

        self.last_command = self.buffer
        self.buffer = ""

    def set_player_life(self, args: list[str]) -> None:
        self.player.life = int(args[0])

    def draw_input(self) -> None:
        position = "" if (mlx.timer % 2 >= 1) else "|"
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main"],
            10,
            690,
            0x0000FF,
            "./" + self.buffer + position
        )

    def draw(self) -> None:
        if (self.enable is True):
            self.draw_input()
