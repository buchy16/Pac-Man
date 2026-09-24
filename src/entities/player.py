from . import Entity
from .. import Maze
from .. import mlx

# i = height (y)
# j = width (x)


class Player(Entity):
    def __init__(self, maze: Maze, life: int = 3) -> None:
        super().__init__(maze)
        self.life = life
        self.super_pacgum = False

        self.i, self.j = self.maze._height // 2, self.maze._width // 2

        self.sprit = mlx.get_tools().mlx_png_file_to_image(
            mlx.mlx_ptr,
            "assets/Entities/J_full.png"
        )[0]

    def move(self) -> None:
        self.i = (self.i + 1) % self.maze._height

    def draw(self) -> None:
        x, y = self.maze.smaze[self.i][self.j]["coor"]
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            self.sprit,
            x - 13,
            y - 13
        )
