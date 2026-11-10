from ..Mlx import mlx
from ..utils.utils import SPECIAL_CHAR, display_string, display_nums
from ..utils.sprites import MENU
from ..data.scores import HighScoreStorage
from .entities.player import Player


class EndScreen():
    def __init__(self, hight_score: HighScoreStorage, player: Player):
        self.hight_score = hight_score
        self.player = player

        self.enable = False
        self.error = False
        self.register_status = 0

        self.last_second = mlx.timer
        self.timer_error = 4.0

        self.buffer = ""

    def enable_disable(self) -> None:
        if (self.enable is False):
            self.enable = True
            mlx.add_key_hook_function(
                self.listen_keyboard,
                "main"
            )
        else:
            self.enable = False
            mlx.rm_key_hook_function(
                self.listen_keyboard,
                "main"
            )

    def listen_keyboard(self, keynum: int) -> None:
        """Process a key event and update the current command buffer.
        Args:
            keynum: Numeric key identifier provided by the graphical library.
        """
        key = mlx.KEYNAME[keynum]

        if (key == "BackSpace"):
            self.buffer = self.buffer[:-1]

        elif (key == "Return"):
            self.register()

        elif (len(key) == 1 and len(self.buffer) < 10):
            if ((ord(key) >= 97 and ord(key) <= 122) or
               (ord(key) >= 48 and ord(key) <= 57)):
                self.buffer += key
        elif (key in SPECIAL_CHAR.keys()):
            if (len(self.buffer) < 10):
                self.buffer += SPECIAL_CHAR[key]

    def register(self) -> None:
        try:
            self.hight_score.add_score(self.buffer, self.player.score)
            self.register_status = 1
        except (ValueError):
            self.error = True
        finally:
            self.buffer = ""

    def update(self) -> int:
        if (self.error is True and mlx.timer - self.last_second >= 1.0):
            self.last_second = mlx.timer
            self.timer_error -= 1.0

            if (self.timer_error <= 0):
                self.error = False
                self.timer_error = 4.0
        return (self.register_status)

    def draw(self, background: int) -> None:
        PTS_LENGHT = 34
        X_MIDDLE_SCREEN = 640
        Y_MIDDLE_SCREEN = 360
        CHAR_SIZE = 14

        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            background,
            0,
            0
        )
        score_lenght = len(str(self.player.score)) * CHAR_SIZE + PTS_LENGHT
        pts_offset = display_nums.display(
            X_MIDDLE_SCREEN - int((score_lenght / 2)),
            Y_MIDDLE_SCREEN,
            "main",
            str(self.player.score)
            )
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            MENU["PTS"],
            pts_offset + 7,
            Y_MIDDLE_SCREEN - 7
        )

        if (self.error is True):
            display_string.display(
                int(X_MIDDLE_SCREEN - (12 * CHAR_SIZE / 2)),
                720 - 180 - 48,
                "main",
                "invalid name"
            )
        else:
            display_string.display(
                int(X_MIDDLE_SCREEN - (15 * CHAR_SIZE / 2)),
                720 - 180 - 48,
                "main",
                "enter your name"
            )
        display_string.display(
            int(X_MIDDLE_SCREEN - (len(self.buffer) * CHAR_SIZE / 2)),
            720 - 180,
            "main",
            self.buffer
            )
