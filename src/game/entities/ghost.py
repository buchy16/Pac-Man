import heapq
import math
from abc import abstractmethod
from .entity import Entity, Direction
from .player import Player
from ..maze import Maze
from ... import mlx
from ...utils import manhattan_dist
from ...directions import DIR_MOVES
from ...sprites import G_WALK_SPRITES

"""
4 types of ghost
    Blinky chases Pac-Man
    Pinky targets a square four squares ahead of Pac-Man
    Inky moves around at random
    Clyde moves around at random and charges at Pac-Man when he is close
"""


class Ghost(Entity):
    def __init__(self, maze: Maze, player: Player, prefix: str,
                 i_start: int, j_start: int, dir_start: Direction,
                 life: int = 1, width: int = 26, height: int = 26) -> None:
        """Initialize a ghost instance

        Parameters
        ----------
        maze : The maze that owns the ghost and provides tile coordinates.
        player : The player the ghost may chase.
        prefix : sprite key, identifying this ghost's sprites.
        i_start, j_start, dir_start : Starting row, column and direction.
        life : default 1 (ghost is alive, else 0)
        width, height : default 26, ghost sprite width and height in pixels
        """
        super().__init__(maze)
        self.player = player
        self.prefix = prefix
        self.life = life
        self.width, self.height = width, height

        self.i_start, self.j_start = i_start, j_start
        self.direction_start = dir_start

        self.i, self.j = self.i_start, self.j_start
        self.direction = self.direction_start

        # position to display in pixels (x, y)
        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]
        self.direction = self.direction_start
        self.target: tuple[int, int]

        # time of the last movement
        self.last_s = mlx.timer

    @abstractmethod
    def get_target(self) -> tuple[int, int]:
        """determines the ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        pass

    def move(self, duration_between_moves: float = 1.0) -> None:
        """call find_path(), in order to move to the next square
        if duration_between_moves (in seconds) has elapsed since the last move
        """
        if mlx.timer - self.last_s >= duration_between_moves:
            target_i, target_j = self.get_target()
            path = self.find_path(
                (self.i, self.j),
                (target_i, target_j)
            )

            # if there is more than one cell in the path (start ≠ finish)
            if len(path) > 1:
                next_i, next_j = path[1]

                if next_i > self.i:
                    self.direction = Direction.SOUTH
                elif next_i < self.i:
                    self.direction = Direction.NORTH
                elif next_j > self.j:
                    self.direction = Direction.EAST
                elif next_j < self.j:
                    self.direction = Direction.WEST

                self.i, self.j = next_i, next_j

            self.last_s = mlx.timer

        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]

    def draw(self) -> None:
        """ animates the ghost by alternating, every 0.25 seconds,
        between two sprites corresponding wich direction is moving
        """
        frame = "1" if (mlx.timer % 0.50 < 0.25) else "2"
        dir_ghost_key = f"{frame}{self.prefix}"

        # displays the sprite centred on the cell
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            G_WALK_SPRITES[dir_ghost_key][self.direction],
            self.x - self.width // 2,
            self.y - self.height // 2
        )

    def find_path(self, start: tuple[int, int],
                  goal: tuple[int, int]) -> list[tuple[int, int]]:
        """Shortest path from start to goal, in cells (i, j).

        Returns : the sorted list of cells, including start and goal;
                  an empty list if no path exists.

        MY VARS
            moves: les 4 déplacements possibles et le bitwise du mur associé
            intermediate_costs: for each cell visited,
                            the smallest number of steps found since the start
            previous_cells: for each cell, the cell we came from,
                            used to reverse path at the end.
            to_visit_heap: priority queue of cells still to be explored
                        returns first the cell with the lowest total score.
        """

        if start == goal:
            return [start]

        intermediate_costs: dict[tuple[int, int], int] = {start: 0}

        previous_cells: dict[tuple[int, int], tuple[int, int] | None] = {}
        previous_cells[start] = None

        estimated_start_to_goal = manhattan_dist(start, goal)
        # int: estimated total cost
        # int: cost from start to this cell
        # tuple[int, int]: this cell's coordinates
        to_visit_heap: list[tuple[int, int, tuple[int, int]]]
        to_visit_heap = [(estimated_start_to_goal, 0, start)]

        while to_visit_heap:
            _, actual_cost_to_current, current_coord = heapq.heappop(
                to_visit_heap
            )
            current_i, current_j = current_coord

            if current_coord == goal:
                break

            # LOWER cost has already been recorded for this cell
            if actual_cost_to_current > intermediate_costs.get(
                current_coord, math.inf
            ):
                continue

            # for each of the 4 neighbouring cells
            for wall, (di, dj) in DIR_MOVES.items():
                neighbour_i, neighbour_j = current_i + di, current_j + dj
                neighbour_coord = (neighbour_i, neighbour_j)

                # if accessible and not already visited
                if (
                    0 <= neighbour_i < self.maze._height
                    and 0 <= neighbour_j < self.maze._width
                    and (self.maze.smaze[current_i][current_j]["code"]
                         & wall == 0)
                ):

                    neighbour_cost: int = intermediate_costs[current_coord] + 1

                    # if this path to this neighbour is shorter
                    # than one already known
                    if neighbour_cost < intermediate_costs.get(
                        neighbour_coord, math.inf
                    ):
                        intermediate_costs[neighbour_coord] = neighbour_cost
                        previous_cells[neighbour_coord] = current_coord
                        total_cost = neighbour_cost + manhattan_dist(
                            neighbour_coord, goal
                        )
                        heapq.heappush(
                            to_visit_heap,
                            (total_cost, neighbour_cost, neighbour_coord)
                        )

        if goal not in previous_cells:
            return []

        # reconstructs the path from the goal to the start
        path: list[tuple[int, int]] = []
        current_step: tuple[int, int] | None = goal
        while current_step is not None:
            path.append(current_step)
            current_step = previous_cells[current_step]
        path.reverse()
        return path
