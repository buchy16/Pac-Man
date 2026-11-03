import logging
from src.Mlx import mlx
from src.game.entities.player import Player
from src.game.entities.ghost_manager import GhostManager
from src.game.gums.pacgum_manager import PacgumManager
from src.utils.utils import SPECIAL_CHAR, Color
from src.game.cheats.commands import (
    Kill, SetPlayerLife, SetPlayerScore, SetPlayerSpeed, FreezeGhosts,
    SetPlayerInvincible, StopTimer, SkipingLevel, Help, ResetAll,
    Command
    )


class Cheat():
    """Manage cheat-mode commands, keyboard input, and their game effects.
    """

    def __init__(self, player: Player, ghosts: GhostManager,
                 pacgums: PacgumManager) -> None:
        """Initialize the cheat manager and its registered commands.

        Args:
            player: Player whose state can be modified by cheat commands.
            ghosts: Ghost manager used by ghost-related commands.
            pacgums: Pacgum manager used to skip the current level.
        """
        self.player = player
        self.ghosts = ghosts
        self.pacgums = pacgums

        self.enable = False

        self.buffer = ""
        self.command_stack: list[str] = [""]
        self.stack_index = -1  # for the last element added on the list

        self.skiping_level = False
        self.timer_frozen = False

        self.commands: dict[str, Command] = {
            "kill": Kill(self),
            "skip-level": SkipingLevel(self),
            "help": Help(self),
            "reset-all": ResetAll(self),
            "lives": SetPlayerLife(self),
            "score": SetPlayerScore(self),
            "speed": SetPlayerSpeed(self),
            "freeze": FreezeGhosts(self),
            "invincible": SetPlayerInvincible(self),
            "stop-timer": StopTimer(self)
        }

# -----------------------------------------------------------------------------
# -----------------------------   LISTENER   ----------------------------------
# -----------------------------------------------------------------------------

    def enable_disable(self) -> None:
        """Toggle cheat mode and register or remove the keyboard listener."""
        if (self.enable is False):
            mlx.add_key_hook_function(
                self.listen_keyboard,
                "main"
            )
            self.enable = True
            # logging.info("(cheat): \033[32mactivated\033[0m")
            self.inform("activated", Color.GREEN)
        else:
            mlx.rm_key_hook_function(
                self.listen_keyboard,
                "main"
            )
            # logging.info("(cheat): \033[31mdeactivated\033[0m")
            self.inform("deactivated", Color.RED)
            self.enable = False

    def listen_keyboard(self, keynum: int) -> None:
        """Process a key event and update the current command buffer.

        Args:
            keynum: Numeric key identifier provided by the graphical library.
        """
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

        elif (len(key) == 1 and len(self.buffer) <= 25):
            if ((ord(key) >= 97 and ord(key) <= 122) or
               (ord(key) >= 48 and ord(key) <= 57)):
                self.buffer += key

        elif (key in SPECIAL_CHAR.keys()):
            self.buffer += SPECIAL_CHAR[key]

# -----------------------------------------------------------------------------
# -------------------------------   COMMAND   ---------------------------------
# -----------------------------------------------------------------------------

    def command_analyser(self) -> None:
        """Parse and execute the command currently stored in the buffer."""
        if (len(self.buffer) <= 0):
            return

        raw_command = self.buffer.split(" ")
        command = raw_command[0]
        args = []
        if (len(raw_command) > 1):
            args = raw_command[1:]

        try:
            self.commands[command].execut(args)
        except (KeyError):
            self.warn("Unkown commande", "consider using help command")
            self.buffer = ""
            return

        self.command_stack.append(self.buffer)
        if (len(self.command_stack) > 6):
            self.command_stack.pop(0)
        self.buffer = ""

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        """Apply pending cheat effects during the game update loop."""
        if (self.skiping_level is True):
            self.skip_level()

    def skip_level(self) -> None:
        """Mark the next remaining pacgum as eaten.

        Once every pacgum has been eaten, clear the pending level-skip state.
        """
        for line in self.pacgums.pacgums:
            for gum in line:
                if (gum.was_eaten is False):
                    gum.was_eaten = True
                    self.pacgums.update_img()
                    return
        self.skiping_level = False

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw_input(self) -> None:
        """Draw the current command buffer and its blinking cursor."""
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
        """Draw the cheat input when cheat mode is enabled."""
        if (self.enable is True):
            self.draw_input()

# -----------------------------------------------------------------------------
# ------------------------------     UTILS   ----------------------------------
# -----------------------------------------------------------------------------

    def set_new_pacgums(self, new_pacgums: PacgumManager) -> None:
        """Replace the pacgum manager used by the level-skip effect.

        Args:
            new_pacgums: Pacgum manager for the newly loaded level.
        """
        self.skiping_level = False
        self.pacgums = new_pacgums

    def warn(self, msg: str, additional: str | None = None) -> None:
        """Log a red warning related to cheat-mode commands.

        Args:
            msg: Main warning message.
            additional: Optional text appended to the warning.
        """
        msg = "\033[31m" + msg + "\033[0m"
        if (additional is not None):
            msg += " " + additional
        logging.warning(f"(cheat): {msg}")

    def inform(self, msg: str, color: Color = Color.NONE,
               additional: str | None = None) -> None:
        """Log an informational cheat-mode message.

        Args:
            msg: Main informational message.
            color: Color used to display the message.
            additional: Optional text appended to the message.
        """
        msg = color.value + msg + "\033[0m"
        if (additional is not None):
            msg += " " + additional
        logging.info(f"(cheat): {msg}")
