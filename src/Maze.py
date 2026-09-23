from mazegenerator import MazeGenerator
from . import mlx
from typing import TypedDict, Dict


class MazeContent(TypedDict):
    code: int
    coor: tuple[int, int]


WALLS = {
    0b0000: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0000.png"),
    0b0001: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0001.png"),
    0b0010: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0010.png"),
    0b0011: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0011.png"),
    0b0100: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0100.png"),
    0b0101: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0101.png"),
    0b0110: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0110.png"),
    0b0111: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0111.png"),
    0b1000: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1000.png"),
    0b1001: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1001.png"),
    0b1010: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1010.png"),
    0b1011: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1011.png"),
    0b1100: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1100.png"),
    0b1101: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1101.png"),
    0b1110: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1110.png"),
    0b1111: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1111.png"),
}


class Maze(MazeGenerator):
    def __init__(self, size: tuple[int, int] = (15, 15), perfect: bool = False,
                 entry_cell: tuple[int, int] = (0, 0),
                 exit_cell: tuple[int, int] = (-1, -1),
                 seed: int = 0):
        super().__init__(size, perfect, entry_cell, exit_cell, seed)
        self.x, self.y = self.set_coordinates()
        self.Smaze = self.generate_Smaze()
        self.maze_img = self.bake_background(self._width, self._height, 24)

    def generate_Smaze(self) -> list[list[Dict[str, MazeContent]]]:
        result = []
        x = self.x + round(24 / 2)
        y = self.y + round(24 / 2)

        for i in range(0, self._height):
            line = []
            for j in range(0, self._width):
                line.append({"code": self._maze[i][j], "coor": (x, y)})
                x += 24
            result.append(line)
            y += 24
            x = 0
        return (result)

    def set_coordinates(self) -> tuple[int, int]:
        middle_x = round(1280 / 2)
        middle_y = round(720 / 2)

        Δx = middle_x - round((self._width * 24) / 2)
        Δy = middle_y - round((self._height * 24) / 2)
        return (Δx, Δy)

    def display_Smaze(self) -> None:
        for i in range(0, self._height):
            for j in range(0, self._width):
                print(f" {self.Smaze[i][j]['coor']} ", end="")
            print()

    def bake_background(self, tiles_width: int, tiles_height: int,
                        tile_size: int = 24):
        total_w = tiles_width * tile_size
        total_h = tiles_height * tile_size
        bg_img = mlx.get_tools().mlx_new_image(mlx.mlx_ptr, total_w, total_h)
        bg_addr, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(bg_img)
        bytes_per_px = bg_bpp // 8
        x, y = 0, 0

        for i in range(tiles_height):
            for j in range(tiles_width):
                code = self.Smaze[i][j]["code"]
                tile_img = WALLS[code][0]
                tile_addr, _, tile_line, _ = (mlx.get_tools().
                                              mlx_get_data_addr(tile_img))

                row_bytes = tile_size * bytes_per_px
                for line in range(tile_size):
                    src_start = line * tile_line
                    src = tile_addr[src_start:src_start + row_bytes]

                    dst_start = (y + line) * bg_line + x * bytes_per_px
                    bg_addr[dst_start:dst_start + row_bytes] = src
                x += 24
            y += 24
            x = 0

        return (bg_img)

    def draw_maze(self) -> None:
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            self.maze_img,
            self.x,
            self.y
        )
