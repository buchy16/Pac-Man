from mazegenerator import MazeGenerator
from . import mlx

# On est pas en RGB mais en BGR


class App():
    def __init__(self) -> None:
        self.number = 0
        mlx.new_window(1280, 720, "main")
        self.middle_X = int(1280 / 2)
        self.middle_Y = int(720 / 2)
        self.img = mlx.get_tools().mlx_png_file_to_image(
            mlx.mlx_ptr,
            "assets/Maze Parts.png"
        )[0]

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        pass

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            self.img,
            0,
            0
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
