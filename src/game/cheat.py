from src.Mlx import mlx
from src.game.entities.player import Player
from src.game.entities.ghost_manager import GhostManager
from src.game.gums.pacgum_manager import PacgumManager
from src.utils.utils import SPECIAL_CHAR


class Cheat():
    def __init__(self, player: Player, ghosts: GhostManager,
                 pacgums: PacgumManager) -> None:
        self.player = player
        self.ghosts = ghosts
        self.pacgums = pacgums

        self.enable = False

        self.buffer = ""
        self.command_stack: list[str] = [""]
        self.stack_index = -1  # for the last element added on the list

        self.skiping_level = False

    def set_new_pacgums(self, new_pacgums: PacgumManager) -> None:
        self.skiping_level = False
        self.pacgums = new_pacgums

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
            self.stack_index = -1
            self.command_analyser()

        elif (key == "Tab"):
            self.buffer = self.command_stack[self.stack_index]
            # index start from the end and decrease (-1 % 6 = 5, -2 % 6 = 4...)
            self.stack_index = (self.stack_index - 1) % len(self.command_stack)

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
        args = []
        if (len(raw_command) > 1):
            args = raw_command[1:]

        if (command == "kill"):
            self.player.life = 0
        elif (command == "reset-all"):
            self.ghosts._reset_all_ghosts()
        elif (command == "lives"):
            self.set_player_life(args)
        elif (command == "score"):
            self.set_player_score(args)
        elif (command == "speed"):
            self.set_player_speed(args)
        elif (command == "freeze"):
            self.freeze_ghosts(args)
        elif (command == "skip-level"):
            self.skiping_level = True
        elif (command == "invincible"):
            # self.set_player_invincible(args)
            pass
        else:
            print("Unkow commande")
            self.buffer = ""
            return

        self.command_stack.append(self.buffer)
        if (len(self.command_stack) > 6):
            self.command_stack.pop(0)
        self.buffer = ""

    def set_player_life(self, args: list[str]) -> None:
        try:
            lives = int(args[0])
            self.player.life = lives
        except (ValueError, IndexError):
            print("invalide arguments")

    def set_player_score(self, args: list[str]) -> None:
        try:
            score = int(args[0])
            self.player.score = score
        except (ValueError, IndexError):
            print("invalide arguments")

    def set_player_speed(self, args: list[str]) -> None:
        try:
            if (args[0] == "reset"):
                speed = 1.0
            else:
                speed = float(args[0])
            self.player.speed = speed
        except (ValueError, IndexError):
            print("invalide arguments")

    def freeze_ghosts(self, args: list[str]) -> None:
        try:
            # quick freeze if no arguments
            if (len(args) <= 0):
                self.ghosts._set_all_ghosts_freeze(True)
                return

            target, boolean = args
            target = target.lower()
            if (boolean == "true" or boolean == "false"):
                boolean = boolean == "true"
            else:
                raise ValueError()

            if (target == "all"):
                self.ghosts._set_all_ghosts_freeze(boolean)
            self.ghosts.ghosts[target.lower()].is_frozen = boolean
        except (ValueError, KeyError, IndexError):
            print("invalide arguments")

    def set_player_invincible(self, args: list[str]) -> None:
        try:
            if (args[0] == "true" or args[0] == "false"):
                boolean = args[0] == "true"
            else:
                raise ValueError()
            self.player.invincible = boolean
        except (ValueError, IndexError):
            print("invalide arguments")

    def update(self) -> None:
        if (self.skiping_level is True):
            self.skip_level()

    def skip_level(self) -> None:
        for line in self.pacgums.pacgums:
            for gum in line:
                if (gum.was_eaten is False):
                    gum.was_eaten = True
                    self.pacgums.update_img()
                    return
        self.skiping_level = False

    def draw_input(self) -> None:
        position = "" if (mlx.timer % 1 >= 0.5) else "|"
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
