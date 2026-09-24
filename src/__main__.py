from . import mlx, Maze
from .parse_config import parsing
from .entities import Player

# On est pas en RGB mais en BGR


class App():
    def __init__(self) -> None:
        self.number = 0
        mlx.new_window(1280, 720, "main")
        self.middle_X = int(1280 / 2)
        self.middle_Y = int(720 / 2)

        self.maze = Maze(size=(15, 15), seed=42)

        self.player = Player(self.maze)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        self.player.move()

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        self.maze.draw_maze()

        self.player.draw()

        # self.maze.display_Smaze()


def main():
    print("begining tests")
    pac_man = App()

    mlx.run(pac_man.update, pac_man.draw)


if __name__ == "__main__":
    parsing("config.json")
    main()
