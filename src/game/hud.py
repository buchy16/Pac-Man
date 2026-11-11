from ..Mlx import mlx
from ..utils.utils import display_nums
from ..utils.sprites import MENU, HUD
from .entities.player import Player


class Hud():
    LIVE_W = 26
    LIVE_H = 22

    def __init__(self, player: Player, level_id: int) -> None:
        """_summary_

        Args:
            player (Player): player class
            level_id (str): curent level to diplay
        """
        self.player = player
        self.player_life = player.life
        self.life_img: int
        self.set_lives_img(self.player_life, 1)

        self.level_id = level_id

    def set_level(self, level_id: int) -> None:
        """Change the level to display

        Args:
            level_id (str): level id
        """
        self.level_id = level_id

    def set_lives_img(self, nb_tiles_width: int, nb_tiles_height: int) -> None:
        """Build an image representing the player's lif

        Args:
            nb_tiles_width (int): number of icons to represent
            nb_tiles_height (int): number or row
        """
        total_w = nb_tiles_width * self.LIVE_W
        total_h = nb_tiles_height * self.LIVE_H
        life_img = mlx.get_tools().mlx_new_image(mlx.mlx_ptr, total_w, total_h)
        bg_ad, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(life_img)
        bytes_per_px = bg_bpp // 8
        x, y = 0, 0

        for i in range(nb_tiles_height):
            for j in range(nb_tiles_width):
                tile_img = HUD["Lives"]
                tile_addr, _, tile_line, _ = (mlx.get_tools().
                                              mlx_get_data_addr(tile_img))

                row_bytes = self.LIVE_W * bytes_per_px
                for line in range(self.LIVE_H):
                    src_start = line * tile_line
                    src = tile_addr[src_start:src_start + row_bytes]

                    dst_start = (y + line) * bg_line + x * bytes_per_px
                    bg_ad[dst_start:dst_start + row_bytes] = src
                x += self.LIVE_W
            y += self.LIVE_H
            x = 0

        self.life_img = life_img

    def update(self) -> None:
        """Check if the player's life changed. If it changed, the lives_img
        will be rebuild
        """
        if (self.player_life != self.player.life and self.player.life > 0):
            self.player_life = self.player.life

            # prevent drawing an absurd amount of life icons
            if (self.player.life > 12):
                self.player_life = 12
            self.destroy_img()
            self.set_lives_img(self.player_life, 1)

    def draw_pacman_lives(self) -> None:
        """Draw life icons according to the player life.
        If the player's life is greater than 12, exp(life icon) will be added
        at the end of the life_img
        """
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            self.life_img,
            0,
            int(39 - (self.LIVE_H / 2))
        )
        if (self.player.life > 12):
            mlx.get_tools().mlx_put_image_to_window(
                    mlx.mlx_ptr,
                    mlx.windows["main"],
                    HUD["exp"],
                    12 * self.LIVE_W,
                    int(39 - (self.LIVE_H / 2))
            )

    def draw(self, timer: float) -> None:
        """Draw the full HUD including, score, remaining life, actual level and
        remaining time

        Args:
            timer (float): time left
        """
        pts_offset = display_nums.display(
            10 - 7,
            10,
            "main",
            str(self.player.score)
            )
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            MENU["PTS"],
            pts_offset + 7,
            0
        )

        # 39 = pts_y + 10 + pcaman lives icon height
        if (self.player.life > 0):
            self.draw_pacman_lives()

        # 55 = pcaman lives icon y + pcaman lives icon height / 2 + 5
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main"],
            0,
            55,
            0x7FCB36,
            f"Level {self.level_id}"
        )
        # 78 = I tried my best :c
        # draw timer
        mlx.get_tools().mlx_string_put(
            mlx.mlx_ptr,
            mlx.windows["main"],
            0,
            78,
            0x0000FF,
            f"time left: {int(timer)}"
        )

    def destroy_img(self) -> None:
        """Destroy the life image and free memory
        """
        mlx.get_tools().mlx_destroy_image(mlx.mlx_ptr, self.life_img)
