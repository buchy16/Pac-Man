from ..Mlx import mlx
from typing import Callable
from ..sprites import MAIN_MENU


class MainMenu():
    def __init__(self):
        mlx.new_window(720, 720, "main_menu")
        self.to_draw: Callable = self.draw_main_menu
        mlx.add_mouse_hook_function(self._update_menu, "main_menu")

        self.menu_state = self.main_menu

        self.game_started = False

        _, x, y = mlx.get_tools().mlx_mouse_get_pos(mlx.windows["main_menu"])
        self.x = x
        self.y = y

    def update(self):
        _, x, y = mlx.get_tools().mlx_mouse_get_pos(mlx.windows["main_menu"])
        self.x = x
        self.y = y

    def _update_menu(self, button, x, y) -> None:
        self.menu_state(button, x, y)

    def main_menu(self, button: int, x: int, y: int) -> None:
        if (button == 1 and (
           (x >= 360 - 180 and x <= 360 + 180) and
           (y >= 144 - 72 and y <= 144 + 72))):
            self.game_started = True
            mlx.close_window("main_menu")
        elif (button == 1 and (
           (x >= 360 - 180 and x <= 360 + 180) and
           (y >= 288 - 72 and y <= 288 + 72))):
            self.menu_state = self.scores_viwer
        elif (button == 1 and (
           (x >= 360 - 180 and x <= 360 + 180) and
           (y >= 432 - 72 and y <= 432 + 72))):
            self.menu_state = self.instructions
        elif (button == 1 and (
           (x >= 360 - 180 and x <= 360 + 180) and
           (y >= 700 - 72 and y <= 700 + 72))):
            mlx.close_app()

    def scores_viwer(self, button: int, x: int, y: int) -> None:
        if (button == 1 and (
           (x >= 360 - 180 and x <= 360 + 180) and
           (y >= 700 - 72 and y <= 700 + 72))):
            self.menu_state = self.main_menu

    def instructions(self, button: int, x: int, y: int) -> None:
        if (button == 1 and (
           (x >= 360 - 180 and x <= 360 + 180) and
           (y >= 700 - 72 and y <= 700 + 72))):
            self.menu_state = self.main_menu

    def draw_main_menu(self):
        if ((self.x >= 360 - 180 and self.x <= 360 + 180) and
           (self.y >= 144 - 72 and self.y <= 144 + 72)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Start Game b"],
                360 - 216,
                144 - 86
            )
        else:
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Start Game"],
                360 - 180,
                144 - 72
            )
        if ((self.x >= 360 - 180 and self.x <= 360 + 180) and
           (self.y >= 288 - 72 and self.y <= 288 + 72)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["View_Highscores b"],
                360 - 216,
                288 - 86
            )
        else:
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["View_Highscores"],
                360 - 180,
                288 - 72
            )
        if ((self.x >= 360 - 180 and self.x <= 360 + 180) and
           (self.y >= 432 - 72 and self.y <= 432 + 72)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Instructions b"],
                360 - 216,
                432 - 86
            )
        else:
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Instructions"],
                360 - 180,
                432 - 72
            )
        if ((self.x >= 360 - 180 and self.x <= 360 + 180) and
           (self.y >= 700 - 72 and self.y <= 700 + 72)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit b"],
                360 - 216,
                700 - 86
            )
        else:
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit"],
                360 - 180,
                700 - 72
            )

    def draw_scores_viwer(self):
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            220,
            360,
            0x0000FF,
            "Score will be dispalyed here"
        )
        if ((self.x >= 360 - 180 and self.x <= 360 + 180) and
           (self.y >= 700 - 72 and self.y <= 700 + 72)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit b"],
                360 - 216,
                700 - 86
            )
        else:
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit"],
                360 - 180,
                700 - 72
            )

    def draw_instructions(self) -> None:
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            240,
            360,
            0x0000FF,
            "Picture of instructions"
        )
        if ((self.x >= 360 - 180 and self.x <= 360 + 180) and
           (self.y >= 700 - 72 and self.y <= 700 + 72)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit b"],
                360 - 216,
                700 - 86
            )
        else:
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit"],
                360 - 180,
                700 - 72
            )

    def draw(self) -> None:
        if (self.menu_state == self.main_menu):
            self.draw_main_menu()
        elif (self.menu_state == self.scores_viwer):
            self.draw_scores_viwer()
        elif (self.menu_state == self.instructions):
            self.draw_instructions()
