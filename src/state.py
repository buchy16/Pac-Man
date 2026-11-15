from abc import ABC, abstractmethod


class State(ABC):
    """Define the interface for a game state."""

    @abstractmethod
    def __init__(self) -> None:
        """Initialize a game state."""
        pass

    @abstractmethod
    def update(self) -> int:
        """Update the state and report whether the stop sequence is active.

        Returns:
            1 if the stop sequence is activated, otherwise 0.
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """Draw the current state."""
        pass

    @abstractmethod
    def unload(self) -> "State":
        """Unload the current state and return the next state."""
        pass
