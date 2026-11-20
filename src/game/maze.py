from mazegenerator import MazeGenerator
from ..utils.sprites import WALLS
from ..Mlx import mlx
from typing import TypedDict


class MazeContent(TypedDict):
    """Represents a single maze cell.

    Attributes:
        code: Binary value describing the walls around the cell.
        coor: Pixel coordinates of the cell in the final rendered maze image.
    """

    code: int
    coor: tuple[int, int]


class Maze(MazeGenerator):
    """Represents a maze that has been generated and is ready to display.

    This class extends the underlying maze generator to produce a richer
    structure containing wall codes, pixel coordinates for each cell, and the
    final assembled image used for MLX rendering.
    """

    def __init__(self, size: tuple[int, int] = (15, 15), perfect: bool = False,
                 entry_cell: tuple[int, int] = (0, 0),
                 exit_cell: tuple[int, int] = (-1, -1),
                 seed: int = 0) -> None:
        """Initialize the maze and prepare it for visual rendering.

        Args:
            size:       Maze dimensions as ``(width, height)``.
            perfect:    If ``True``, generate a perfect maze without loops.
            entry_cell: Coordinates of the entry cell.
            exit_cell:  Coordinates of the exit cell. ``(-1, -1)`` means no
                        explicit exit is defined.
            seed:       Random seed used to generate the maze.
        """
        super().__init__(size, perfect, entry_cell, exit_cell, seed)
        self.x, self.y = self.set_coordinates()
        self.smaze = self.generate_smaze()
        self.maze_img = self.bake_background(self._width, self._height, 48)

    def generate_smaze(self) -> list[list[MazeContent]]:
        """Build the maze grid with each cell's code and coordinates.

        Returns:
            list[list[dict[str, MazeContent]]]: A list of rows.
            Each cell stores a dictionary with the keys ``code`` and ``coor``.
        """
        result = []
        x = self.x + round(48 / 2)
        y = self.y + round(48 / 2)

        for i in range(0, self._height):
            line = []
            for j in range(0, self._width):
                data: MazeContent = {"code": self._maze[i][j], "coor": (x, y)}
                line.append(data)
                x += 48
            result.append(line)
            y += 48
            x = self.x + round(48 / 2)
        return result

    def set_coordinates(self) -> tuple[int, int]:
        """Compute the offset required to center the maze in the window.

        Returns:
            tuple[int, int]: A tuple ``(offset_x, offset_y)`` used to place the
            maze at the center of the screen.
        """
        middle_x = round(1280 / 2)
        middle_y = round(720 / 2)

        Δx = middle_x - round((self._width * 48) / 2)
        Δy = middle_y - round((self._height * 48) / 2)
        return (Δx, Δy)

    def display_Smaze(self) -> None:
        """Print the maze grid to the console.
        """
        for i in range(0, self._height):
            for j in range(0, self._width):
                print(f" {self.smaze[i][j]['coor']} ", end="")
            print()

    def bake_background(self, tiles_width: int, tiles_height: int,
                        tile_size: int = 48) -> int:
        """Compose the maze background by assembling wall tiles.

        Args:
            tiles_width: Number of columns in the maze.
            tiles_height: Number of rows in the maze.
            tile_size: Size in pixels of each square tile.

        Returns:
            int: MLX image identifier for the generated background.
        """
        total_w = tiles_width * tile_size
        total_h = tiles_height * tile_size
        bg_img: int = mlx.get_tools().mlx_new_image(mlx.mlx_ptr,
                                                    total_w, total_h)
        bg_addr, bg_bpp, bg_line, _ = mlx.get_tools().mlx_get_data_addr(bg_img)
        bytes_per_px = bg_bpp // 8
        x, y = 0, 0

        for i in range(tiles_height):
            for j in range(tiles_width):
                code = self.smaze[i][j]["code"]
                tile_img = WALLS[code][0]
                tile_addr, _, tile_line, _ = (mlx.get_tools().
                                              mlx_get_data_addr(tile_img))

                row_bytes = tile_size * bytes_per_px
                for line in range(tile_size):
                    src_start = line * tile_line
                    src = tile_addr[src_start:src_start + row_bytes]

                    dst_start = (y + line) * bg_line + x * bytes_per_px
                    bg_addr[dst_start:dst_start + row_bytes] = src
                x += 48
            y += 48
            x = 0

        return bg_img

    def draw_maze(self) -> None:
        """Display the maze in the main application window.
        """
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            self.maze_img,
            self.x,
            self.y
        )

    def regenerate_maze(self, size: tuple[int, int] = (15, 15),
                        perfect: bool = False,
                        entry_cell: tuple[int, int] = (0, 0),
                        exit_cell: tuple[int, int] = (-1, -1),
                        seed: int = 0) -> None:
        """Generate a new maze

        Args:
            size:       Maze dimensions as ``(width, height)``.
            perfect:    If ``True``, generate a perfect maze without loops.
            entry_cell: Coordinates of the entry cell.
            exit_cell:  Coordinates of the exit cell. ``(-1, -1)`` means no
                        explicit exit is defined.
            seed:       Random seed used to generate the maze.
        """
        # ---------------------------------------------------------------------
        # Original Maze re-generation
        self._width = size[0]
        self._height = size[1]
        self._perfect = perfect
        self._seed = seed
        self._entryx = (entry_cell[0]
                        if 0 <= entry_cell[0] < self._width else 0)
        self._entryy = (entry_cell[1]
                        if 0 <= entry_cell[1] < self._height else 0)
        self._exitx = (exit_cell[0]
                       if 0 <= exit_cell[0] < self._width else self._width-1)
        self._exity = (exit_cell[1]
                       if 0 <= exit_cell[1] < self._height else self._height-1)
        self._maze: list[list[int]] = []
        self._path: list[list[int]] = []
        self._shortest_path: str | bool = False
        self.generate(self._seed)

        # ---------------------------------------------------------------------
        # Custom Maze re-generation
        self.x, self.y = self.set_coordinates()
        self.smaze = self.generate_smaze()
        self.destroy_background()
        self.maze_img = self.bake_background(self._width, self._height, 48)

    def destroy_background(self) -> None:
        """Destroy the background image and free memory
        """
        mlx.get_tools().mlx_destroy_image(mlx.mlx_ptr, self.maze_img)
