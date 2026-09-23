from . import mlx, Maze

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

        self.maze = Maze(size=(30, 30), seed=42)

# -----------------------------------------------------------------------------
# -------------------------------   UPDATE   ----------------------------------
# -----------------------------------------------------------------------------

    def update(self) -> None:
        pass

# -----------------------------------------------------------------------------
# -------------------------------     DRAW   ----------------------------------
# -----------------------------------------------------------------------------

    def draw(self) -> None:
        self.maze.draw_maze()
        pass


def main():
    print("begining tests")
    pac_man = App()

    mlx.run(pac_man.update, pac_man.draw)


if __name__ == "__main__":
    main()
