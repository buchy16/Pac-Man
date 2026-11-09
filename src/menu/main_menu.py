from typing import Callable
from ..Mlx import mlx
from ..utils.sprites import MENU
from ..data.parse_config import GameConfig
from ..utils.utils import display_nums, display_string
from ..state import State

# Srceen middle x coordinate
S_MIDDLE_X = 360

# normal button (use for draw and selection) half size
HALF_WIDTH = 180
HALF_HEIGHT = 72

# big button (only use for draw when the mouse is on it) half size
BIG_HALF_WIDTH = 216
BIG_HALF_HEIGHT = 86


class MainMenu(State):
    """Manage the main menu state and drawing logic.

    Attributes:
        config: Game configuration used to render the instruction screen.
        to_draw: Callable used by the game loop to draw the current menu state.
        menu_state: Current handler for menu interactions.
        game_started: Flag indicating whether the game has been launched.
        x: Current mouse x coordinate in the menu window.
        y: Current mouse y coordinate in the menu window.
    """

    def __init__(self, config: GameConfig) -> None:
        """Initialize the main menu window and input handlers.

        Args:
            config: Game configuration used by the instructions screen.

        Returns:
            None.
        """
        self.config = config

        mlx.new_window(720, 720, "MENU")
        self.to_draw: Callable = self.draw_MENU
        mlx.add_mouse_hook_function(self._update_menu, "MENU")

        self.menu_state = self.MENU

        self.game_started = False

        _, x, y = mlx.get_tools().mlx_mouse_get_pos(mlx.windows["MENU"])
        self.x = x
        self.y = y

    def update(self) -> int:
        """Refresh the cached mouse position.

        Returns:
            int: 1 if the user want to quit this state, else 0 ongoing
        """
        _, x, y = mlx.get_tools().mlx_mouse_get_pos(mlx.windows["MENU"])
        self.x = x
        self.y = y

        if (self.game_started is True):
            return (1)
        return (0)

    def _update_menu(self, button: int, x: int, y: int) -> None:
        """Dispatch a mouse event to the active menu handler.

        Args:
            button: Mouse button identifier received from the hook.
            x: Mouse x coordinate at the time of the event.
            y: Mouse y coordinate at the time of the event.

        Returns:
            None.
        """
        self.menu_state(button, x, y)

    def MENU(self, button: int, x: int, y: int) -> None:
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
            self.menu_state = self.MENU

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
            self.menu_state = self.MENU

    def draw_MENU(self):
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
                mlx.windows["MENU"],
                MENU["Start Game b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                144 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["MENU"],
                MENU["Start Game"],
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
                mlx.windows["MENU"],
                MENU["View_Highscores b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                288 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["MENU"],
                MENU["View_Highscores"],
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
                mlx.windows["MENU"],
                MENU["Instructions b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                432 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["MENU"],
                MENU["Instructions"],
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
                mlx.windows["MENU"],
                MENU["Exit b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                700 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["MENU"],
                MENU["Exit"],
                S_MIDDLE_X - HALF_WIDTH,
                700 - HALF_HEIGHT
            )

    def draw_scores_viwer(self):
        """Draw the highscores screen.

        Returns:
            None.
        """
        # mlx.get_tools().mlx_string_put(
        #     mlx.mlx_ptr,
        #     mlx.windows["MENU"],
        #     220,
        #     S_MIDDLE_X,
        #     0x0000FF,
        #     "Score will be dispalyed here"
        # )
        display_string(220, S_MIDDLE_X, "MENU", "Hello world")

        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Exit
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and self.x <=
             S_MIDDLE_X + HALF_WIDTH) and
           (self.y >= 700 - HALF_HEIGHT and self.y <= 700 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["MENU"],
                MENU["Exit b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                700 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["MENU"],
                MENU["Exit"],
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
            mlx.windows["MENU"],
            MENU["Instructions_img"],
            S_MIDDLE_X - 250,
            0
        )
        # Display point per pacgum followed by PTS
        x_pts = display_nums(110 + 242, 391, "MENU",
                             str(self.config.points_per_pacgum))
        mlx.get_tools().mlx_put_image_to_window(mlx.mlx_ptr,
                                                mlx.windows["MENU"],
                                                MENU["PTS"],
                                                x_pts, 391 - 7)

        # Display point per pacgum followed by PTS
        x_pts = display_nums(110 + 242, 428, "MENU",
                             str(self.config.points_per_super_pacgum))
        mlx.get_tools().mlx_put_image_to_window(mlx.mlx_ptr,
                                                mlx.windows["MENU"],
                                                MENU["PTS"],
                                                x_pts, 428 - 7)

        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Exit
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and self.x <=
             S_MIDDLE_X + HALF_WIDTH) and
           (self.y >= 700 - HALF_HEIGHT and self.y <= 700 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["MENU"],
                MENU["Exit b"],
                S_MIDDLE_X - BIG_HALF_WIDTH,
                700 - BIG_HALF_HEIGHT
            )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["MENU"],
                MENU["Exit"],
                S_MIDDLE_X - HALF_WIDTH,
                700 - HALF_HEIGHT
            )

    def draw(self) -> None:
        """Draw the currently selected menu screen.

        Returns:
            None.
        """
        if (self.menu_state == self.MENU):
            self.draw_MENU()
        elif (self.menu_state == self.scores_viwer):
            self.draw_scores_viwer()
        elif (self.menu_state == self.instructions):
            self.draw_instructions()

    def unload(self) -> State:
        from ..game import Game
        mlx.close_window("MENU")
        return (Game(self.config))
