from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    # returns 1 if the stop sequence is activated
    def update(self) -> int:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def unload(self) -> "State":
        pass
