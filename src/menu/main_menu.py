from typing import Callable
from ..Mlx import mlx
from ..utils.sprites import MAIN_MENU
from ..data.parse_config import GameConfig
from ..utils.utils import display_nums

# Srceen middle x coordinate
S_MIDDLE_X = 360

# normal button (use for draw and selection) half size
HALF_WIDTH = 180
HALF_HEIGHT = 72

# big button (only use for draw when the mouse is on it) half size
BIG_HALF_WIDTH = 216
BIG_HALF_HEIGHT = 86


class MainMenu():
    """Manage the main menu state and drawing logic.

    Attributes:
        config: Game configuration used to render the instruction screen.
        to_draw: Callable used by the game loop to draw the current menu state.
        menu_state: Current handler for menu interactions.
        game_started: Flag indicating whether the game has been launched.
        x: Current mouse x coordinate in the menu window.
        y: Current mouse y coordinate in the menu window.
    """

    def __init__(self, config: GameConfig):
        """Initialize the main menu window and input handlers.

        Args:
            config: Game configuration used by the instructions screen.

        Returns:
            None.
        """
        self.config = config

        mlx.new_window(720, 720, "main_menu")
        self.to_draw: Callable = self.draw_main_menu
        mlx.add_mouse_hook_function(self._update_menu, "main_menu")

        self.menu_state = self.main_menu

        self.game_started = False

        _, x, y = mlx.get_tools().mlx_mouse_get_pos(mlx.windows["main_menu"])
        self.x = x
        self.y = y

    def update(self):
        """Refresh the cached mouse position.

        Returns:
            None.
        """
        _, x, y = mlx.get_tools().mlx_mouse_get_pos(mlx.windows["main_menu"])
        self.x = x
        self.y = y

    def _update_menu(self, button, x, y) -> None:
        """Dispatch a mouse event to the active menu handler.

        Args:
            button: Mouse button identifier received from the hook.
            x: Mouse x coordinate at the time of the event.
            y: Mouse y coordinate at the time of the event.

        Returns:
            None.
        """
        self.menu_state(button, x, y)

    def main_menu(self, button: int, x: int, y: int) -> None:
        """Handle clicks on the main menu screen.

        Args:
            button: Mouse button identifier. Left click is expected.
            x: Mouse x coordinate.
            y: Mouse y coordinate.

        Returns:
            None.
        """
        # Check if the mouse click was on the surface area of ​​the button
        # Start Game
        if (button == 1 and (
           (x >= S_MIDDLE_X - HALF_WIDTH and x <= S_MIDDLE_X + HALF_WIDTH) and
           (y >= 144 - HALF_HEIGHT and y <= 144 + HALF_HEIGHT))):
            self.game_started = True
            mlx.close_window("main_menu")

        # Check if the mouse click was on the surface area of ​​the button
        # View Highscores
        elif (button == 1 and (
           (x >= S_MIDDLE_X - HALF_WIDTH and x <= S_MIDDLE_X + HALF_WIDTH) and
           (y >= 288 - HALF_HEIGHT and y <= 288 + HALF_HEIGHT))):
            self.menu_state = self.scores_viwer

        # Check if the mouse click was on the surface area of ​​the button
        # Instructions
        elif (button == 1 and (
           (x >= S_MIDDLE_X - HALF_WIDTH and x <= S_MIDDLE_X + HALF_WIDTH) and
           (y >= 432 - HALF_HEIGHT and y <= 432 + HALF_HEIGHT))):
            self.menu_state = self.instructions

        # Check if the mouse click was on the surface area of ​​the button Exit
        elif (button == 1 and (
           (x >= S_MIDDLE_X - HALF_WIDTH and x <= S_MIDDLE_X + HALF_WIDTH) and
           (y >= 700 - HALF_HEIGHT and y <= 700 + HALF_HEIGHT))):
            mlx.close_app()

    def scores_viwer(self, button: int, x: int, y: int) -> None:
        """Handle interactions for the highscores screen.

        Args:
            button: Mouse button identifier. Left click is expected.
            x: Mouse x coordinate.
            y: Mouse y coordinate.

        Returns:
            None.
        """
        # Check if the mouse click was on the surface area of ​​the button Exit
        if (button == 1 and (
           (x >= S_MIDDLE_X - HALF_WIDTH and x <= S_MIDDLE_X + HALF_WIDTH) and
           (y >= 700 - HALF_HEIGHT and y <= 700 + HALF_HEIGHT))):
            self.menu_state = self.main_menu

    def instructions(self, button: int, x: int, y: int) -> None:
        """Handle interactions for the instructions screen.

        Args:
            button: Mouse button identifier. Left click is expected.
            x: Mouse x coordinate.
            y: Mouse y coordinate.

        Returns:
            None.
        """
        # Check if the mouse click was on the surface area of ​​the button Exit
        if (button == 1 and (
           (x >= S_MIDDLE_X - HALF_WIDTH and x <= S_MIDDLE_X + HALF_WIDTH) and
           (y >= 700 - HALF_HEIGHT and y <= 700 + HALF_HEIGHT))):
            self.menu_state = self.main_menu

    def draw_main_menu(self):
        """Draw the main menu screen.

        Returns:
            None.
        """
        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Sart Game
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and self.x <=
             S_MIDDLE_X + HALF_WIDTH) and
           (self.y >= 144 - HALF_HEIGHT and self.y <= 144 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Start Game b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                144 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Start Game"],
                S_MIDDLE_X - HALF_WIDTH,
                144 - HALF_HEIGHT
            )

        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button View_Highscores
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and self.x <=
             S_MIDDLE_X + HALF_WIDTH) and
           (self.y >= 288 - HALF_HEIGHT and self.y <= 288 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["View_Highscores b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                288 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["View_Highscores"],
                S_MIDDLE_X - HALF_WIDTH,
                288 - HALF_HEIGHT
            )

        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Instructions
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and self.x <=
             S_MIDDLE_X + HALF_WIDTH) and
           (self.y >= 432 - HALF_HEIGHT and self.y <= 432 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Instructions b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                432 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Instructions"],
                S_MIDDLE_X - HALF_WIDTH,
                432 - HALF_HEIGHT
            )

        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Exit
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and self.x <=
             S_MIDDLE_X + HALF_WIDTH) and
           (self.y >= 700 - HALF_HEIGHT and self.y <= 700 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                700 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit"],
                S_MIDDLE_X - HALF_WIDTH,
                700 - HALF_HEIGHT
            )

    def draw_scores_viwer(self):
        """Draw the highscores screen.

        Returns:
            None.
        """
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            220,
            S_MIDDLE_X,
            0x0000FF,
            "Score will be dispalyed here"
        )
        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Exit
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and self.x <=
             S_MIDDLE_X + HALF_WIDTH) and
           (self.y >= 700 - HALF_HEIGHT and self.y <= 700 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                700 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit"],
                S_MIDDLE_X - HALF_WIDTH,
                700 - HALF_HEIGHT
            )

    def draw_instructions(self) -> None:
        """Draw the instructions screen.

        Returns:
            None.
        """
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main_menu"],
            MAIN_MENU["Instructions_img"],
            S_MIDDLE_X - 250,
            0
        )
        # Display point per pacgum followed by PTS
        x_pts = display_nums(110 + 242, 391, "main_menu",
                             str(self.config.points_per_pacgum))
        mlx.get_tools().mlx_put_image_to_window(mlx.mlx_ptr,
                                                mlx.windows["main_menu"],
                                                MAIN_MENU["PTS"],
                                                x_pts, 391 - 7)

        # Display point per pacgum followed by PTS
        x_pts = display_nums(110 + 242, 428, "main_menu",
                             str(self.config.points_per_super_pacgum))
        mlx.get_tools().mlx_put_image_to_window(mlx.mlx_ptr,
                                                mlx.windows["main_menu"],
                                                MAIN_MENU["PTS"],
                                                x_pts, 428 - 7)

        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Exit
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and self.x <=
             S_MIDDLE_X + HALF_WIDTH) and
           (self.y >= 700 - HALF_HEIGHT and self.y <= 700 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                700 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main_menu"],
                MAIN_MENU["Exit"],
                S_MIDDLE_X - HALF_WIDTH,
                700 - HALF_HEIGHT
            )

    def draw(self) -> None:
        """Draw the currently selected menu screen.

        Returns:
            None.
        """
        if (self.menu_state == self.main_menu):
            self.draw_main_menu()
        elif (self.menu_state == self.scores_viwer):
            self.draw_scores_viwer()
        elif (self.menu_state == self.instructions):
            self.draw_instructions()
