from .entity import Entity
from ..maze import Maze
from ...utils.sprites import J_WALK_SPRIT
from ...Mlx import mlx
from math import ceil
from ...utils.directions import Direction
from .entity import Slide_State


# i = height (y)
# j = width (x)


class Player(Entity):
    """Represent the player character and manage its movement and sprites."""

    SUPER_P_TIMER = 15.0

    def __init__(self, maze: Maze, life: int = 3) -> None:
        """Initialize the player in the center of the maze.

        Args:
            maze: Maze in which the player moves.
            life: Initial number of lives.
        """
        super().__init__(maze)
        self.life = life
        self.invincible = False
        self.super_pacgum = False
        self.score = 0

        self.i = ceil(self.maze._height / 2) - 1
        self.j = ceil(self.maze._width / 2) - 1
        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]
        self.destination = (self.i, self.j)
        self.direction = Direction.NONE
        self.draw_direction = self.direction

        self.speed = 1.0

        mlx.add_key_hook_function(
            self._update_direction,
            "main"
        )

        self.last_s = mlx.timer  # last second for super pacgum
        self.timer = Player.SUPER_P_TIMER

    def _update_direction(self, keynum: int) -> None:
        """Update the movement direction from a keyboard event.

        Args:
            keynum: Numeric identifier of the pressed key.
        """
        if (mlx.KEYNAME[keynum] == "Up"):
            self.direction = Direction.NORTH
            # print("North")
        elif (mlx.KEYNAME[keynum] == "Down"):
            self.direction = Direction.SOUTH
            # print("South")
        elif (mlx.KEYNAME[keynum] == "Left"):
            self.direction = Direction.WEST
            # print("WEST")
        elif (mlx.KEYNAME[keynum] == "Right"):
            self.direction = Direction.EAST
            # print("Est")

    def reset(self) -> None:
        """Return the player to the starting position and reset its state."""
        self.i = ceil(self.maze._height / 2) - 1
        self.j = ceil(self.maze._width / 2) - 1
        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]
        self.direction = Direction.NONE
        self.draw_direction = self.direction
        self.slide_state = Slide_State.NONE

        self.super_pacgum = False
        self.timer = self.SUPER_P_TIMER

    def player_hit(self) -> None:
        """Remove a life and reset the player when it is not invincible."""
        if (self.invincible is False):
            self.life -= 1
            self.reset()

    def super_pacgam(self) -> None:
        """Update the remaining duration of the super pacgum effect."""
        if (self.super_pacgum is True):
            if (self.timer <= 0):
                self.super_pacgum = False
                self.timer = Player.SUPER_P_TIMER
            else:
                self.timer -= 1

    def move(self) -> None:
        """Move the player according to its direction and current state."""
        time = mlx.timer

        if (time - self.last_s >= 1.0):
            self.super_pacgam()
            self.last_s = time

        if (self.slide_state == Slide_State.SLIDING):
            self.slide()

        if (self.slide_state == Slide_State.NONE):
            next_i, next_j = self.i, self.j
            if (self.direction == Direction.SOUTH and
                    self.maze.smaze[self.i][self.j]["code"] & 0b0100 == 0):
                next_i = (self.i + 1) % self.maze._height

            elif (self.direction == Direction.NORTH and
                    self.maze.smaze[self.i][self.j]["code"] & 0b0001 == 0):
                next_i = (self.i - 1) % self.maze._height

            elif (self.direction == Direction.WEST and
                    self.maze.smaze[self.i][self.j]["code"] & 0b1000 == 0):
                next_j = (self.j - 1) % self.maze._width

            elif (self.direction == Direction.EAST and
                    self.maze.smaze[self.i][self.j]["code"] & 0b0010 == 0):
                next_j = (self.j + 1) % self.maze._width

            self.draw_direction = self.direction
            self.set_destination(next_i, next_j)

    def draw_Est(self) -> None:
        """Draw the player facing east with its walking animation."""
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
        """Draw the player facing west with its walking animation."""
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
        """Draw the player facing north with its walking animation."""
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
        """Draw the player facing south with its walking animation."""
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
        """Draw the player using the sprite for its current direction."""
        if (self.draw_direction == Direction.WEST):
            self.draw_West()
        elif (self.draw_direction == Direction.NORTH):
            self.draw_North()
        elif (self.draw_direction == Direction.SOUTH):
            self.draw_South()
        else:
            self.draw_Est()
