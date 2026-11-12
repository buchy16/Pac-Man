"""Build and display cached text and numeric images."""

import logging
from abc import ABC, abstractmethod
from ..Mlx import mlx
from .sprites import DIGITS, ALPHA


class Displayer(ABC):
    """Provide shared image-building and display functionality."""

    CHAR_SIZE = 14

    def __init__(self) -> None:
        """Initialize the cache used to store generated images."""
        self.assests_save: dict[str, int] = {}

    @abstractmethod
    def _build_img(self, string: str) -> None:
        """Build and cache an image representing ``string``."""
        pass

    def display(self, x: int, y: int, window: str, string: str) -> int:
        """Display ``string`` in a window and return the next x-coordinate."""
        if (len(string) <= 0):
            return (0)

        try:
            string = string.lower()

            # build the image and add it to the dictionary if it
            # doesn't already exist
            if (self.assests_save.get(string) is None):
                self._build_img(string)

            mlx.get_tools().mlx_put_image_to_window(
                mlx.mlx_ptr,
                mlx.windows[window],
                self.assests_save[string],
                x,
                y - 7
                )
        except (KeyError):
            logging.error(f"Can't display {string}")
        return (x + (len(string) * self.CHAR_SIZE))

    def unload_assets(self) -> None:
        """Destroy all images currently stored in the cache."""
        for asset in self.assests_save.values():
            mlx.get_tools().mlx_destroy_image(mlx.mlx_ptr, asset)


class DisplayString(Displayer):
    """Create images containing alphabetic characters and digits."""

    alpha_char = "abcdefghijklmnopqrstuvwxyz 0123456789-."

    def __init__(self) -> None:
        """Initialize the string displayer and its image cache."""
        super().__init__()

    def _build_img(self, string: str) -> None:
        """Build and cache an image from the alphabet sprite atlas."""
        nb_tiles_width = len(string)

        total_w = nb_tiles_width * self.CHAR_SIZE
        total_h = self.CHAR_SIZE
        atals = ALPHA

        img = mlx.get_tools().mlx_new_image(mlx.mlx_ptr, total_w, total_h)
        bg_addr, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(img)
        atlas_addr, _, atlas_line, _ = (mlx.get_tools().
                                        mlx_get_data_addr(atals))
        bytes_per_px = bg_bpp // 8
        x = 0
        for i in range(nb_tiles_width):
            img_x = (self.alpha_char.find(string[i]) % 6) * 14
            img_y = (self.alpha_char.find(string[i]) // 6) * 14
            if (img_x != -14 and img_y != -14):
                # target the first pixel of the letter
                letter_pos = (img_y * atlas_line) + (img_x * bytes_per_px)

                row_bytes = self.CHAR_SIZE * bytes_per_px
                for line in range(self.CHAR_SIZE):
                    src_start = letter_pos + (line * atlas_line)
                    src = atlas_addr[src_start:src_start + row_bytes]
                    dst_start = line * bg_line + x * bytes_per_px
                    bg_addr[dst_start:dst_start + row_bytes] = src
            x += self.CHAR_SIZE

        if (img is not None):
            self.assests_save[string] = img


class DisplayNums(Displayer):
    """Create images containing numeric characters."""

    def __init__(self) -> None:
        """Initialize the numeric displayer and its image cache."""
        super().__init__()

    def _build_img(self, string: str) -> None:
        """Build and cache an image from the digit sprites."""
        nb_tiles_width = len(string)

        total_w = nb_tiles_width * self.CHAR_SIZE
        total_h = self.CHAR_SIZE
        img = mlx.get_tools().mlx_new_image(mlx.mlx_ptr, total_w, total_h)
        bg_addr, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(img)
        bytes_per_px = bg_bpp // 8
        x = 0
        for i in range(nb_tiles_width):
            tile_img = DIGITS[string[i]]
            tile_addr, _, tile_line, _ = (mlx.get_tools().
                                          mlx_get_data_addr(tile_img))
            row_bytes = self.CHAR_SIZE * bytes_per_px
            for line in range(self.CHAR_SIZE):
                src_start = line * tile_line
                src = tile_addr[src_start:src_start + row_bytes]
                dst_start = line * bg_line + x * bytes_per_px
                bg_addr[dst_start:dst_start + row_bytes] = src
            x += self.CHAR_SIZE

        if (img is not None):
            self.assests_save[string] = img
