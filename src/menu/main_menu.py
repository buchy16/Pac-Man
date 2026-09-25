from ..Mlx import mlx
from typing import Callable


class MainMenu():
    def __init__(self):
        mlx.new_window(720, 720, "main_menu")
        self.to_draw: Callable = self.draw_main_menu
        mlx.add_mouse_hook_function(self._update_menu, "main_menu")

        self.menu_state = self.main_menu

    def update(self):
        pass

    def _update_menu(self, button, x, y) -> None:
        self.menu_state(button, x, y)

    def main_menu(self, button: int, x: int, y: int) -> None:
        if (button == 1):
            self.menu_state = self.scores_viwer

    def scores_viwer(self, button: int, x: int, y: int) -> None:
        if (button == 1):
            self.menu_state = self.main_menu

    def instructions(self, button: int, x: int, y: int) -> None:
        pass

    def draw_main_menu(self):
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            360,
            144,
            0x0000FF,
            "S"
        )
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            360,
            288,
            0x0000FF,
            "V"
        )
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            360,
            432,
            0x0000FF,
            "I"
        )
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            360,
            576,
            0x0000FF,
            "E"
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
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            360,
            700,
            0x0000FF,
            "E"
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

    def draw(self) -> None:
        if (self.menu_state == self.main_menu):
            self.draw_main_menu()
        elif (self.menu_state == self.scores_viwer):
            self.draw_scores_viwer()
        elif (self.menu_state == self.instructions):
            self.draw_instructions()
