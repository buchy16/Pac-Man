from .gum import Gum
from .pacgum import Pacgum
from .super_pacgum import SuperPacgum
from ..entities import Player
from ..maze import Maze
from ...Mlx import mlx
from ...sprites import PACGUMS

# i = height (y)
# j = width (x)


class PacgumManager():
    def __init__(self, player: Player, maze: Maze, pacgum_pts: int,
                 s_pacgum_pts: int):
        self.player = player
        self.maze = maze

        # matrix of the same size as the maze
        self.pacgums = self.init_pacgums(pacgum_pts, s_pacgum_pts)

        self.pacgums_img = self.update_img(self.maze._width, self.maze._height)

    def init_pacgums(self, pacgum_pts: int,
                     s_pacgum_pts: int) -> list[list[Gum | None]]:
        matrix = []

        for i in range(0, self.maze._height):
            line = []
            for j in range(0, self.maze._width):
                # if the cell is fuly closed, no pacgum, None insted
                if (self.maze.maze[i][j] == 0b1111):
                    line.append(None)
                else:
                    line.append(Pacgum(self.maze, i, j, pacgum_pts))
            matrix.append(line)

        # Set Super pacgum on each edge of the maze
        matrix[0][0] = SuperPacgum(self.maze, 0, 0, s_pacgum_pts)
        matrix[0][-1] = SuperPacgum(self.maze, 0, self.maze._width - 1,
                                    s_pacgum_pts)
        matrix[-1][0] = SuperPacgum(self.maze, self.maze._height - 1, 0,
                                    s_pacgum_pts)
        matrix[-1][-1] = SuperPacgum(self.maze, self.maze._height - 1,
                                     self.maze._width - 1, s_pacgum_pts)

        # remove the pacgum where the player spawn
        matrix[self.player.i][self.player.j] = None

        return (matrix)

    def update_img(self, tiles_width: int, tiles_height: int,
                   tile_size: int = 48) -> int:

        total_w = tiles_width * tile_size
        total_h = tiles_height * tile_size
        pg_img = mlx.get_tools().mlx_new_image(mlx.mlx_ptr, total_w, total_h)
        pg_addr, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(pg_img)
        bytes_per_px = bg_bpp // 8
        x, y = 0, 0

        for i in range(tiles_height):
            for j in range(tiles_width):
                cell = self.pacgums[i][j]
                if (isinstance(cell, SuperPacgum)):
                    tile_img = PACGUMS["Super pacgum"]
                elif (isinstance(cell, Pacgum)):
                    tile_img = PACGUMS["Pacgum"]
                else:
                    tile_img = PACGUMS["No pacgum"]

                tile_addr, _, tile_line, _ = (mlx.get_tools().
                                              mlx_get_data_addr(tile_img))

                row_bytes = tile_size * bytes_per_px
                for line in range(tile_size):
                    src_start = line * tile_line
                    src = tile_addr[src_start:src_start + row_bytes]

                    dst_start = (y + line) * bg_line + x * bytes_per_px
                    pg_addr[dst_start:dst_start + row_bytes] = src
                x += 48
            y += 48
            x = 0

        return pg_img

    def colsion_cell(self) -> None:
        pacgum = self.pacgums[self.player.i][self.player.j]

        if (pacgum is not None):
            pacgum.eaten(self.player)
            self.pacgums[self.player.i][self.player.j] = None
            self.pacgums_img = self.update_img(self.maze._width,
                                               self.maze._height)

    def update(self) -> None:
        self.colsion_cell()

    def darw(self) -> None:
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            self.pacgums_img,
            self.maze.x,
            self.maze.y
        )

    def display_pacgums(self) -> None:
        for line in self.pacgums:
            for gum in line:
                print(f"[{gum.points}] ", end="")
            print()
        print()
