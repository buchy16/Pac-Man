"""Command objects used by the game's cheat mode."""

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.utils.utils import Color
if (TYPE_CHECKING):
    from src.game.cheats.cheat import Cheat


class Command(ABC):
    """Base class for commands executable through cheat mode.
    """

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize a command bound to a cheat manager.

        Args:
            cheat: Cheat manager whose game state the command can modify.
        """
        self.cheat = cheat
        self.manual: str

    @abstractmethod
    def execut(self, args: list[str] = []) -> None:
        """Execute the command with the supplied arguments.

        Args:
            args: Command-line arguments entered by the player.
        """
        pass

    def warn(self, msg: str, additional: str | None = None) -> None:
        """Log a red warning related to command execution.

        Args:
            msg: Main warning message.
            additional: Optional text appended to the warning.
        """
        msg = "\033[31m" + msg + "\033[0m"
        if (additional is not None):
            msg += " " + additional
        logging.warning(f"(cheat): {msg}")

    def inform(self, msg: str, color: "Color" = Color.NONE,
               additional: str | None = None) -> None:
        """Log an informational message related to command execution.

        Args:
            msg: Main informational message.
            color: Color used to display the message.
            additional: Optional text appended to the message.
        """
        msg = color.value + msg + "\033[0m"
        if (additional is not None):
            msg += " " + additional
        logging.info(f"(cheat): {msg}")


class Kill(Command):
    """Command that immediately eliminates the player."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the player-kill command.

        Args:
            cheat: Cheat manager whose player is targeted.
        """
        super().__init__(cheat)
        self.manual = "kill:\nKill the player"

    def execut(self, args: list[str] = []) -> None:
        """Set the player's remaining lives to zero.

        Args:
            args: Ignored command arguments.
        """
        self.cheat.player.life = 0


class SkipingLevel(Command):
    """Command that requests skipping the current level."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the level-skipping command.

        Args:
            cheat: Cheat manager whose level state is targeted.
        """
        super().__init__(cheat)
        self.manual = "skip-level:\nSkip the curent level"

    def execut(self, args: list[str] = []) -> None:
        """Enable the pending level-skip effect.

        Args:
            args: Ignored command arguments.
        """
        self.cheat.skiping_level = True


class Help(Command):
    """Command that displays the manual for every registered command."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the help command.

        Args:
            cheat: Cheat manager containing the registered commands.
        """
        super().__init__(cheat)
        self.manual = "help:\nDsiplay all commad manual"

    def execut(self, args: list[str] = []) -> None:
        """Log the manual for all registered cheat commands.

        Args:
            args: Ignored command arguments.
        """
        msg = "MANUAL\n"
        for command in self.cheat.commands.values():
            msg += command.manual + "\n\n"
        self.inform(msg)


class ResetAll(Command):
    """Command that resets every ghost to its initial corner."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the ghost-reset command.

        Args:
            cheat: Cheat manager whose ghosts are targeted.
        """
        super().__init__(cheat)
        self.manual = "reset-all:\nReset all ghosts and set their position " \
                      "back to their respective corner"

    def execut(self, args: list[str] = []) -> None:
        """Reset all ghosts to their respective starting positions.

        Args:
            args: Ignored command arguments.
        """
        self.cheat.ghosts._reset_all_ghosts()


class SetPlayerLife(Command):
    """Command that sets the player's number of lives."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the player-life command.

        Args:
            cheat: Cheat manager whose player is targeted.
        """
        super().__init__(cheat)
        self.manual = "lives:\nChange player's life value\nargs:\n\tlife: int"

    def execut(self, args: list[str] = []) -> None:
        """Set the player's lives from the first argument.

        Args:
            args: A list whose first item must be an integer life value.
        """
        try:
            lives = int(args[0])
            self.cheat.player.life = lives
        except (ValueError, IndexError):
            self.warn("invalide arguments")


class SetPlayerScore(Command):
    """Command that sets the player's score."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the player-score command.

        Args:
            cheat: Cheat manager whose player is targeted.
        """
        super().__init__(cheat)
        self.manual = "score:\nChange player's score " \
                      "value\nargs:\n\t score: int"

    def execut(self, args: list[str] = []) -> None:
        """Set the player's score from the first argument.

        Args:
            args: A list whose first item must be an integer score.
        """
        try:
            score = int(args[0])
            self.cheat.player.score = score
        except (ValueError, IndexError):
            self.warn("invalide arguments")


class SetPlayerSpeed(Command):
    """Command that sets or resets the player's movement speed."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the player-speed command.

        Args:
            cheat: Cheat manager whose player is targeted.
        """
        super().__init__(cheat)
        self.manual = "speed:\nChange player's speed " \
                      "value\nargs:\n\t speed: float | str (reset can be used)"

    def execut(self, args: list[str] = []) -> None:
        """Set the player's speed, or reset it with ``reset``.

        Args:
            args: A list whose first item is a float or ``reset``.
        """
        try:
            if (args[0] == "reset"):
                speed = 1.0
            else:
                speed = float(args[0])
            self.cheat.player.speed = speed
        except (ValueError, IndexError):
            self.warn("invalide arguments")


class FreezeGhosts(Command):
    """Command that freezes all ghosts or one selected ghost."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the ghost-freezing command.

        Args:
            cheat: Cheat manager whose ghosts are targeted.
        """
        super().__init__(cheat)
        self.manual = "freeze:\nFreeze ghosts" \
                      "(they can't move)\nargs:\n\t" \
                      "target: str (ghost's name or all)\n\t" \
                      "bool: bool"

    def execut(self, args: list[str] = []) -> None:
        """Set the frozen state of ghosts.

        With no arguments, freeze every ghost. Otherwise, the arguments must
        contain a ghost name (or ``all``) and ``true`` or ``false``.

        Args:
            args: Optional target and boolean frozen-state arguments.
        """
        try:
            # quick freeze if no arguments
            if (len(args) <= 0):
                self.cheat.ghosts._set_all_ghosts_freeze(True)
                return

            target, boolean_arg = args
            target = target.lower()
            if (boolean_arg == "true" or boolean_arg == "false"):
                boolean = boolean_arg == "true"
            else:
                raise ValueError()

            if (target == "all"):
                self.cheat.ghosts._set_all_ghosts_freeze(boolean)
            self.cheat.ghosts.ghosts[target.lower()].is_frozen = boolean
        except (ValueError, KeyError, IndexError):
            self.warn("invalide arguments")


class SetPlayerInvincible(Command):
    """Command that enables or disables player invincibility."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the invincibility command.

        Args:
            cheat: Cheat manager whose player is targeted.
        """
        super().__init__(cheat)
        self.manual = "invincible:\nSet if the player can be hit by ghosts" \
                      "\nargs:\n\t bool: bool"

    def execut(self, args: list[str] = []) -> None:
        """Set whether the player can be hit by ghosts.

        Args:
            args: A list whose first item must be ``true`` or ``false``.
        """
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
    """Command that pauses or resumes the game timer."""

    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the timer command.

        Args:
            cheat: Cheat manager whose timer state is targeted.
        """
        super().__init__(cheat)
        self.manual = "stop-timer:\nStop the timer or not" \
                      "\nargs:\n\t bool: bool"

    def execut(self, args: list[str] = []) -> None:
        """Set whether the game timer is frozen.

        Args:
            args: A list whose first item must be ``true`` or ``false``.
        """
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


class Super(Command):
    def __init__(self, cheat: "Cheat") -> None:
        """Initialize the Super command.

        Args:
            cheat: Cheat manager whose player is targeted.
        """
        super().__init__(cheat)
        self.manual = "super:\nSet Pacman to super Pacman or not" \
                      "\nargs:\n\t bool: bool"

    def execut(self, args: list[str] = []) -> None:
        """Set whether player is in state super Pacman.

        Args:
            args: A list whose first item must be ``true`` or ``false``.
        """
        try:
            if (args[0] == "true"):
                self.cheat.player.super_pacgum = True
                self.cheat.player.timer = self.cheat.player.SUPER_P_TIMER
            elif (args[0] == "false"):
                self.cheat.player.super_pacgum = False
                self.cheat.player.timer = self.cheat.player.SUPER_P_TIMER
            else:
                raise ValueError()
        except (ValueError, IndexError):
            self.warn("invalide arguments")
