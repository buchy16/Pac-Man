from .gum import Gum
from .pacgum import Pacgum
from .super_pacgum import SuperPacgum
from ..entities import Player
from ..maze import Maze
from ...Mlx import mlx
from ...utils.sprites import PACGUMS

# i = height (y)
# j = width (x)


class PacgumManager():
    """Manage pacgum placement, rendering, and collection.

    The manager builds the pacgum matrix from the maze layout, keeps the
    rendered image in sync, and handles pacgum collection when the player
    enters a tile.
    """

    def __init__(self, player: Player, maze: Maze, pacgum_pts: int,
                 s_pacgum_pts: int):
        """Initialize the pacgum manager.

        Parameters
        ----------
        player : Player
            The player instance used to detect collisions and update score.
        maze : Maze
            The maze instance used to build the pacgum matrix and render it.
        pacgum_pts : int
            The number of points awarded for a regular pacgum.
        s_pacgum_pts : int
            The number of points awarded for a super pacgum.
        """
        self.player = player
        self.maze = maze

        # matrix of the same size as the maze
        # Contains a pacgum or None if nothing
        self.pacgums: list[list[Gum]] = self.init_pacgums(pacgum_pts,
                                                          s_pacgum_pts)

        self.pacgums_img = self.create_img(self.maze._width, self.maze._height)

    def init_pacgums(self, pacgum_pts: int,
                     s_pacgum_pts: int) -> list[list[Gum]]:
        """Build the pacgum matrix from the maze layout.

        Parameters
        ----------
        pacgum_pts : int
            The number of points assigned to each regular pacgum.
        s_pacgum_pts : int
            The number of points assigned to each super pacgum.

        Returns
        -------
        list[list[Gum | None]]
            A 2D matrix containing pacgums, super pacgums, or ``None`` where
            no collectible should exist.
        """
        matrix: list[list[Gum]] = []

        for i in range(0, self.maze._height):
            line = []
            for j in range(0, self.maze._width):
                # if the cell is fuly closed, no pacgum, None insted
                if (self.maze.maze[i][j] == 0b1111):
                    gum = Pacgum(self.maze, i, j, pacgum_pts)
                    gum.was_eaten = True
                    line.append(gum)
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
        matrix[self.player.i][self.player.j].was_eaten = True

        return (matrix)

    def create_img(self, tiles_width: int, tiles_height: int,
                   tile_size: int = 48) -> int:
        """Build the pacgum layer image from the current matrix.

        Parameters
        ----------
        tiles_width : int
            Width of the rendered maze in tiles.
        tiles_height : int
            Height of the rendered maze in tiles.
        tile_size : int, optional
            Size in pixels of each tile, by default 48.

        Returns
        -------
        int
            The MLX image handle containing the rendered pacgum layer.
        """

        total_w = tiles_width * tile_size
        total_h = tiles_height * tile_size
        pg_img = mlx.get_tools().mlx_new_image(mlx.mlx_ptr, total_w, total_h)
        pg_addr, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(pg_img)
        bytes_per_px = bg_bpp // 8
        x, y = 0, 0

        for i in range(tiles_height):
            for j in range(tiles_width):
                cell = self.pacgums[i][j]
                if (cell.was_eaten is False):
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

    def update_img(self) -> None:
        """Rebuild the pacgum layer image from the current matrix
        """
        self.destroy_img()
        self.pacgums_img = self.create_img(self.maze._width,
                                           self.maze._height)

    def colsion_cell(self) -> None:
        """Handle a pacgum collision on the player current tile.

        If a pacgum exists on the player tile, it is consumed, removed from
        the matrix, and the cached image is rebuilt.
        """
        pacgum = self.pacgums[self.player.i][self.player.j]

        if (pacgum.was_eaten is False):
            pacgum.eaten(self.player)
            self.pacgums[self.player.i][self.player.j].was_eaten = True
            self.update_img()

    def update(self) -> None:
        """Update the pacgum manager state for the current frame.
        """
        self.colsion_cell()

    def draw(self) -> None:
        """Draw the pacgum layer to the main window.
        """
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            self.pacgums_img,
            self.maze.x,
            self.maze.y
        )

    def display_pacgums(self) -> None:
        """Print the pacgum matrix to standard output for debugging.
        """
        for line in self.pacgums:
            for gum in line:
                print(f"[{gum.points}] ", end="")
            print()
        print()

    def all_gums_eaten(self) -> bool:
        """Check if all pacgums were eaten

        Returns:
            bool: True if all pacgums were eaten, else False
        """
        for i in range(0, self.maze._height):
            for j in range(0, self.maze._width):
                if (self.pacgums[i][j].was_eaten is False):
                    return (False)
        return (True)

    def destroy_img(self) -> None:
        """Destroy pacgums image and free memory
        """
        mlx.get_tools().mlx_destroy_image(mlx.mlx_ptr, self.pacgums_img)
