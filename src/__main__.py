from mazegenerator import MazeGenerator
from . import mlx

# On est pas en RGB mais en BGR


class App():
    def __init__(self) -> None:
        self.number = 0
        mlx.new_window(256, 256, "main")

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        pass

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        if (mlx.timer % 2 <= 0.5):
            mlx.get_tools().mlx_string_put(
                mlx.mlx_ptr,
                mlx.windows["main"],
                128,
                128,
                0x0000FF,  # couleur BGR en Hexa
                str(mlx.timer)
            )
        elif (mlx.timer % 2 > 0.5 and mlx.timer % 2 <= 1):
            mlx.get_tools().mlx_string_put(
                mlx.mlx_ptr,
                mlx.windows["main"],
                128,
                128,
                0x00FFFF,
                str(mlx.timer)
            )
        elif (mlx.timer % 2 > 1 and mlx.timer % 2 <= 1.5):
            mlx.get_tools().mlx_string_put(
                mlx.mlx_ptr,
                mlx.windows["main"],
                128,
                128,
                0xFF0000,
                str(mlx.timer)
            )
        elif (mlx.timer % 2 > 1.5):
            mlx.get_tools().mlx_string_put(
                mlx.mlx_ptr,
                mlx.windows["main"],
                128,
                128,
                0xFF00FF,
                str(mlx.timer)
            )


def get_maze(display: bool = False) -> None:
    maze = MazeGenerator()
    maze.generate()
    if (display is True):
        print(maze.maze)


def main():
    print("begining tests")
    get_maze()
    pac_man = App()

    mlx.run(pac_man.update, pac_man.draw)


if __name__ == "__main__":
    main()
