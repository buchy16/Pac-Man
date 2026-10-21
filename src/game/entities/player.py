from . import Entity
from ... import Maze
from ... import J_WALK_SPRIT
from ... import mlx
from enum import Enum, auto
from math import ceil
from ...utils.directions import Direction


# i = height (y)
# j = width (x)


# class Direction(Enum):
#     NORTH = auto()
#     SOUTH = auto()
#     WEST = auto()
#     EST = auto()
#     NONE = auto()


class Player(Entity):
    def __init__(self, maze: Maze, life: int = 3) -> None:
        super().__init__(maze)
        self.life = life
        self.super_pacgum = False
        self.score = 0

        self.i = ceil(self.maze._height / 2) - 1
        self.j = ceil(self.maze._width / 2) - 1
        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]
        self.direction: Direction = Direction.NONE

        mlx.add_key_hook_function(
            self._update_direction,
            "main"
        )

        self.last_s = mlx.timer

    def _update_direction(self, keynum: int) -> None:
        # print("hi ?")
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
            self.direction = Direction.EAST
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
                self.j = (self.j - 1) % self.maze._width

            elif (self.direction == Direction.EAST and
                    self.maze.smaze[self.i][self.j]["code"] & 0b0010 == 0):
                self.j = (self.j + 1) % self.maze._width
            self.last_s = mlx.timer
        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]

    def draw_Est(self) -> None:
        if (mlx.timer % 0.80 < 0.20):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["0J"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.20 and mlx.timer % 0.80 < 0.40):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["1J_Est"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.40 and mlx.timer % 0.80 < 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["2J_Est"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["1J_Est"],
                self.x - 13,
                self.y - 13
            )

    def draw_West(self) -> None:
        if (mlx.timer % 0.80 < 0.20):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["0J"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.20 and mlx.timer % 0.80 < 0.40):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["1J_West"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.40 and mlx.timer % 0.80 < 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["2J_West"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["1J_West"],
                self.x - 13,
                self.y - 13
            )

    def draw_North(self) -> None:
        if (mlx.timer % 0.80 < 0.20):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["0J"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.20 and mlx.timer % 0.80 < 0.40):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["1J_North"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.40 and mlx.timer % 0.80 < 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["2J_North"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["1J_North"],
                self.x - 13,
                self.y - 13
            )

    def draw_South(self) -> None:
        if (mlx.timer % 0.80 < 0.20):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["0J"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.20 and mlx.timer % 0.80 < 0.40):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["1J_South"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.40 and mlx.timer % 0.80 < 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["2J_South"],
                self.x - 13,
                self.y - 13
            )
        elif (mlx.timer % 0.80 >= 0.60):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                J_WALK_SPRIT["1J_South"],
                self.x - 13,
                self.y - 13
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
