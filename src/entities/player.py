from . import Entity
from .. import Maze
from .. import mlx
from enum import Enum, auto

# i = height (y)
# j = width (x)

WALK_SPRIT = {
    "0J": (mlx.get_tools().
           mlx_png_file_to_image(mlx.mlx_ptr, "assets/Entities/0J.png")[0]),
    "1J_Est": (mlx.get_tools().
               mlx_png_file_to_image(mlx.mlx_ptr,
                                     "assets/Entities/1J_Est.png")[0]),
    "1J_North": (mlx.get_tools().
                 mlx_png_file_to_image(mlx.mlx_ptr,
                                       "assets/Entities/1J_North.png")[0]),
    "1J_South": (mlx.get_tools().
                 mlx_png_file_to_image(mlx.mlx_ptr,
                                       "assets/Entities/1J_South.png")[0]),
    "1J_West": (mlx.get_tools().
                mlx_png_file_to_image(mlx.mlx_ptr,
                                      "assets/Entities/1J_West.png")[0]),
    "2J_Est": (mlx.get_tools().
               mlx_png_file_to_image(mlx.mlx_ptr,
                                     "assets/Entities/2J_Est.png")[0]),
    "2J_North": (mlx.get_tools().
                 mlx_png_file_to_image(mlx.mlx_ptr,
                                       "assets/Entities/2J_North.png")[0]),
    "2J_South": (mlx.get_tools().
                 mlx_png_file_to_image(mlx.mlx_ptr,
                                       "assets/Entities/2J_South.png")[0]),
    "2J_West": (mlx.get_tools().
                mlx_png_file_to_image(mlx.mlx_ptr,
                                      "assets/Entities/2J_West.png")[0]),
}


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    WEST = auto()
    EST = auto()
    NONE = auto()


class Player(Entity):
    def __init__(self, maze: Maze, life: int = 3) -> None:
        super().__init__(maze)
        self.life = life
        self.super_pacgum = False

        self.i, self.j = self.maze._height // 2, self.maze._width // 2
        self.direction: Direction = Direction.NONE

        mlx.add_key_hook_function(
            self._update_direction,
            "main"
        )

        self.last_s = mlx.timer

    def _update_direction(self, keynum: int) -> None:
        if (mlx.KEYNAME[keynum] == "w"):
            self.direction = Direction.NORTH
            # print("North")
        elif (mlx.KEYNAME[keynum] == "s"):
            self.direction = Direction.SOUTH
            # print("South")
        elif (mlx.KEYNAME[keynum] == "a"):
            self.direction = Direction.WEST
            # print("WEST")
        elif (mlx.KEYNAME[keynum] == "d"):
            self.direction = Direction.EST
            # print("Est")

    def move(self) -> None:
        if (mlx.timer - self.last_s >= 1):
            if (self.direction == Direction.SOUTH and
                    self.maze.smaze[self.i][self.j]["code"] & 0b0100 == 0):
                self.i = (self.i + 1) % self.maze._height

            elif (self.direction == Direction.NORTH and
                    self.maze.smaze[self.i][self.j]["code"] & 0b0001 == 0):
                self.i = (self.i - 1) % self.maze._height

            elif (self.direction == Direction.WEST and
                    self.maze.smaze[self.i][self.j]["code"] & 0b1000 == 0):
                self.j = (self.j - 1) % self.maze._height

            elif (self.direction == Direction.EST and
                    self.maze.smaze[self.i][self.j]["code"] & 0b0010 == 0):
                self.j = (self.j + 1) % self.maze._height
            self.last_s = mlx.timer

    def draw_Est(self) -> None:
        x, y = self.maze.smaze[self.i][self.j]["coor"]

        if (mlx.timer % 0.80 < 0.20):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["0J"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.20 and mlx.timer % 0.80 < 0.40):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["1J_Est"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.40 and mlx.timer % 0.80 < 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["2J_Est"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["1J_Est"],
                x - 13,
                y - 13
            )

    def draw_West(self) -> None:
        x, y = self.maze.smaze[self.i][self.j]["coor"]

        if (mlx.timer % 0.80 < 0.20):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["0J"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.20 and mlx.timer % 0.80 < 0.40):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["1J_West"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.40 and mlx.timer % 0.80 < 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["2J_West"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["1J_West"],
                x - 13,
                y - 13
            )

    def draw_North(self) -> None:
        x, y = self.maze.smaze[self.i][self.j]["coor"]

        if (mlx.timer % 0.80 < 0.20):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["0J"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.20 and mlx.timer % 0.80 < 0.40):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["1J_North"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.40 and mlx.timer % 0.80 < 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["2J_North"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["1J_North"],
                x - 13,
                y - 13
            )

    def draw_South(self) -> None:
        x, y = self.maze.smaze[self.i][self.j]["coor"]

        if (mlx.timer % 0.80 < 0.20):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["0J"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.20 and mlx.timer % 0.80 < 0.40):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["1J_South"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.40 and mlx.timer % 0.80 < 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["2J_South"],
                x - 13,
                y - 13
            )
        elif (mlx.timer % 0.80 >= 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                WALK_SPRIT["1J_South"],
                x - 13,
                y - 13
            )

    def draw(self) -> None:
        x, y = self.maze.smaze[self.i][self.j]["coor"]

        if (self.direction == Direction.WEST):
            self.draw_West()
        elif (self.direction == Direction.NORTH):
            self.draw_North()
        elif (self.direction == Direction.SOUTH):
            self.draw_South()
        else:
            self.draw_Est()
