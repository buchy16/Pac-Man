from ..Mlx import mlx
from ..utils.sprites import MENU, BACKGROUNDS


# Srceen middle x and y coordinates
S_MIDDLE_X = 640
S_MIDDLE_Y = 360

# normal button (use for draw and selection) half size
HALF_WIDTH = 180
HALF_HEIGHT = 72

# big button (only use for draw when the mouse is on it) half size
B_HALF_WIDTH = 216
B_HALF_HEIGHT = 86

# Background size
BG_HALF_WITDH = 550
BG_HALF_HEIGHT = 360


class PausMenu():
    """Manage the pause menu state, input, and rendering."""

    def __init__(self) -> None:
        """Initialize the pause menu in its inactive state."""
        self.x = 0
        self.y = 0

        self.pause = False

        self.exiting = 0  # 0 flase, 1 true

    def update_mouse(self) -> None:
        """Update the stored mouse position from the main window."""
        _, x, y = mlx.get_tools().mlx_mouse_get_pos(mlx.windows["main"])
        self.x = x
        self.y = y

    def activate_mouse_butons(self) -> None:
        """Register the pause menu mouse callback."""
        mlx.add_mouse_hook_function(self.update_paus_menu, "main")

    def deactivate_mouse_butons(self) -> None:
        """Remove the pause menu mouse callback."""
        mlx.rm_mouse_hook_function(self.update_paus_menu, "main")

    def activate_pause(self) -> None:
        """Activate the pause menu and its mouse input."""
        if (self.pause is False):
            self.pause = True
            self.activate_mouse_butons()

    def deactivate_pause(self) -> None:
        """Deactivate the pause menu and remove its mouse input."""
        self.deactivate_mouse_butons()
        self.pause = False

    def update_paus_menu(self, button: int, x: int, y: int) -> None:
        """Handle a mouse click on the pause menu buttons.

        Args:
            button: Mouse button identifier.
            x: Horizontal position of the click.
            y: Vertical position of the click.
        """
        if ((x >= S_MIDDLE_X - HALF_WIDTH and
             x <= S_MIDDLE_X + HALF_WIDTH) and
            (y >= 240 - HALF_HEIGHT and
             y <= 240 + HALF_HEIGHT)):
            self.deactivate_pause()

        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and
             self.x <= S_MIDDLE_X + HALF_WIDTH) and
            (self.y >= 480 - HALF_HEIGHT and
             self.y <= 480 + HALF_HEIGHT)):
            self.exiting = 1

    def draw_paus_menu(self) -> None:
        """Draw the pause menu and highlight buttons under the mouse."""
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            BACKGROUNDS["Pause menu"],
            S_MIDDLE_X - BG_HALF_WITDH,
            S_MIDDLE_Y - BG_HALF_HEIGHT
        )

        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Resume
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and
             self.x <= S_MIDDLE_X + HALF_WIDTH) and
            (self.y >= 240 - HALF_HEIGHT and
             self.y <= 240 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                MENU["Resume b"],
                S_MIDDLE_X - B_HALF_WIDTH,
                240 - B_HALF_HEIGHT
                )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                        mlx.mlx_ptr,
                        mlx.windows["main"],
                        MENU["Resume"],
                        S_MIDDLE_X - HALF_WIDTH,
                        240 - HALF_HEIGHT
                    )

        # Draw a bigger version of the button if the mouse is on the surface
        # area of the button Exit
        if ((self.x >= S_MIDDLE_X - HALF_WIDTH and
             self.x <= S_MIDDLE_X + HALF_WIDTH) and
            (self.y >= 480 - HALF_HEIGHT and
             self.y <= 480 + HALF_HEIGHT)):
            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows["main"],
                MENU["Exit b"],
                S_MIDDLE_X - B_HALF_WIDTH,
                480 - B_HALF_HEIGHT
                )
        else:
            # normal size
            mlx.get_tools().mlx_put_image_to_window(
                        mlx.mlx_ptr,
                        mlx.windows["main"],
                        MENU["Exit"],
                        S_MIDDLE_X - HALF_WIDTH,
                        480 - HALF_HEIGHT
                    )
