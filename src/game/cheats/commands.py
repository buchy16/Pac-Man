import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.utils.utils import Color
if (TYPE_CHECKING):
    from src.game.cheats.cheat import Cheat


class Command(ABC):
    def __init__(self, cheat: "Cheat") -> None:
        self.cheat = cheat
        self.manual: str

    @abstractmethod
    def execut(self, args: list[str] = []) -> None:
        pass

    def warn(self, msg: str, additional: str | None = None) -> None:
        msg = "\033[31m" + msg + "\033[0m"
        if (additional is not None):
            msg += " " + additional
        logging.warning(f"(cheat): {msg}")

    def inform(self, msg: str, color: "Color" = Color.NONE,
               additional: str | None = None) -> None:
        msg = color.value + msg + "\033[0m"
        if (additional is not None):
            msg += " " + additional
        logging.info(f"(cheat): {msg}")


class Kill(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "kill:\nKill the player"

    def execut(self, args: list[str] = []) -> None:
        self.cheat.player.life = 0


class SkipingLevel(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "skip-level:\nSkip the curent level"

    def execut(self, args: list[str] = []) -> None:
        self.cheat.skiping_level = True


class Help(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "help:\nDsiplay all commad manual"

    def execut(self, args: list[str] = []):
        msg = "MANUAL\n"
        for command in self.cheat.commands.values():
            msg += command.manual + "\n\n"
        self.inform(msg)


class ResetAll(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "reset-all:\nReset all ghosts and set their position " \
                      "back to their respective corner"

    def execut(self, args: list[str] = []) -> None:
        self.cheat.ghosts._reset_all_ghosts()


class SetPlayerLife(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "lives:\nChange player's life value\nargs:\n\tlife: int"

    def execut(self, args: list[str] = []) -> None:
        try:
            lives = int(args[0])
            self.cheat.player.life = lives
        except (ValueError, IndexError):
            self.warn("invalide arguments")


class SetPlayerScore(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "score:\nChange player's score " \
                      "value\nargs:\n\t score: int"

    def execut(self, args: list[str] = []) -> None:
        try:
            score = int(args[0])
            self.cheat.player.score = score
        except (ValueError, IndexError):
            self.warn("invalide arguments")


class SetPlayerSpeed(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "speed:\nChange player's speed " \
                      "value\nargs:\n\t speed: float"

    def execut(self, args: list[str] = []) -> None:
        try:
            if (args[0] == "reset"):
                speed = 1.0
            else:
                speed = float(args[0])
            self.cheat.player.speed = speed
        except (ValueError, IndexError):
            self.warn("invalide arguments")


class FreezeGhosts(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "freeze:\nFreeze ghosts" \
                      "(they can't move)\nargs:\n\t" \
                      "target: str (ghost's name or all)\n\t" \
                      "bool: bool"

    def execut(self, args: list[str] = []) -> None:
        try:
            # quick freeze if no arguments
            if (len(args) <= 0):
                self.cheat.ghosts._set_all_ghosts_freeze(True)
                return

            target, boolean = args
            target = target.lower()
            if (boolean == "true" or boolean == "false"):
                boolean = boolean == "true"
            else:
                raise ValueError()

            if (target == "all"):
                self.cheat.ghosts._set_all_ghosts_freeze(boolean)
            self.cheat.ghosts.ghosts[target.lower()].is_frozen = boolean
        except (ValueError, KeyError, IndexError):
            self.warn("invalide arguments")


class SetPlayerInvincible(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "invincible:\nSet if the player can be hit by ghosts" \
                      "\nargs:\n\t bool: bool"

    def execut(self, args: list[str] = []) -> None:
        try:
            if (args[0] == "true" or args[0] == "false"):
                boolean = args[0] == "true"
            else:
                raise ValueError()
            self.cheat.player.invincible = boolean

            if (boolean is True):
                self.inform("TRUE", Color.GREEN, ": invincible")
            else:
                self.inform("FALSE", Color.RED, ": invincible")
        except (ValueError, IndexError):
            self.warn("invalide arguments")


class StopTimer(Command):
    def __init__(self, cheat: "Cheat") -> None:
        super().__init__(cheat)
        self.manual = "stop-timer:\nStop the timer or not" \
                      "\nargs:\n\t bool: bool"

    def execut(self, args: list[str] = []) -> None:
        try:
            if (args[0] == "true" or args[0] == "false"):
                boolean = args[0] == "true"
            else:
                raise ValueError()
            self.cheat.timer_frozen = boolean

            if (boolean is True):
                self.inform("TRUE", Color.GREEN, ": timer stoped")
            else:
                self.inform("FALSE", Color.RED, ": timer stoped")
        except (ValueError, IndexError):
            self.warn("invalide arguments")
