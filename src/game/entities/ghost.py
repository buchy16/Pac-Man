import heapq
import math
from enum import Enum, auto
from .entity import Entity, Direction
from .player import Player
from .targets import TargetStrategy
from ..maze import Maze
from ... import mlx
from ...utils.utils import manhattan_dist
from ...utils.directions import DIR_MOVES
from ...utils.sprites import G_WALK_SPRITES


class GhostState(Enum):
    CHASER = auto()       # Pursues its target (Pac-Man, random or other)
    FRIGHTENED = auto()   # Escapes from Pac-Man (far corner, random or other)
    DEAD = auto()         # Returns and remains at his corner for DEATH_DELAY


"""
4 types of ghost
    Blinky chases Pac-Man
    Pinky targets a square four squares ahead of Pac-Man
    Inky chases Pac-Man in a team with Blinky
    Clyde moves around at random and charges at Pac-Man when he is close
"""


class Ghost(Entity):
    DEATH_DELAY: int = 10  # in seconds
    SNAIL_SPEED: float = 1.5
    FAST_SPEED: float = 0.75
    ROCKET_SPEED: float = 0.15

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 corner_start: tuple[int, int], dir_start: Direction,
                 chase_strategy: TargetStrategy,
                 flee_strategy: TargetStrategy) -> None:
        """Initialize a ghost instance

        Parameters
        ----------
        maze: The maze that owns the ghost and provides tile coordinates.
        player: The player the ghost may chase.
        prefix: Sprite key, identifying this ghost's sprites.
        speed: Duration between moves, in seconds.
        corner_start, dir_start: Starting (row,column) and direction.
        chase_strategy: Targeting used when the ghost is CHASER.
        flee_strategy: Targeting used when the ghost is FRIGHTENED
                       (also used to go back home when DEAD).

        Other attributes
        ----------
        x, y: Position to display in pixels
        direction: The direction in which the ghost is heading (north, east...)
        target: Coordinates in the grid of the target cell
        state: State of the ghost (CHASER, FRIGHTENED, DEAD)
        strategy: The strategy currently in use (chase or flee)
        is_frozen: To immobilise the ghost in cheat mode
        last_s: time of the last movement
        last_death: time of the last death
        """
        super().__init__(maze)
        self.player = player
        self.prefix = prefix
        self.normal_speed = speed
        self.speed = speed
        self.i_corner, self.j_corner = corner_start
        self.direction_start = dir_start

        self.i, self.j = corner_start
        self.direction = self.direction_start
        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]
        self.target: tuple[int, int] = corner_start
        self.state = GhostState.CHASER
        self.is_frozen: bool = False
        self.last_s = mlx.timer
        self.last_death: float = 0.0

        self.chase_strategy: TargetStrategy = chase_strategy
        self.flee_strategy: TargetStrategy = flee_strategy
        self.strategy: TargetStrategy = self.chase_strategy

# ===========================================================================
#
# ===========================================================================

    def _get_corner(self, ghost_name: str) -> int:
        if ghost_name == "pinky":
            return (0)
        if ghost_name == "blinky":
            return (1)
        if ghost_name == "inky":
            return (2)
        if ghost_name == "clyde":
            return (3)
        return (0)

    def reset(self, corners: list[tuple[int, int]], name: str) -> None:
        """Puts the ghost back on its starting square, as a fresh CHASER.
        (is_frozen is left untouched: it is controlled by the cheat mode)
        """
        id_corner = self._get_corner(name)
        self.i_corner, self.j_corner = corners[id_corner]
        self.i, self.j = corners[id_corner]
        self.direction = self.direction_start
        self.target = corners[id_corner]
        self.state = GhostState.CHASER
        self.strategy = self.chase_strategy
        self.speed = self.normal_speed
        self.last_death = 0.0
        self.last_s = mlx.timer
        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]

# ===========================================================================
#                                                       METHODS for COLLISION
# ===========================================================================

    def hit_player(self) -> bool:
        """
        Returns:
            True when Pac-Man and the ghost are on the same square on the grid
        """
        return (self.i == self.player.i and self.j == self.player.j)

    def die(self) -> None:
        """Changes the state of the dying ghost and starts the timer."""
        self.state = GhostState.DEAD
        self.speed = self.ROCKET_SPEED
        self.last_death = mlx.timer

# ===========================================================================
#                                                                 MOVE & DRAW
# ===========================================================================

    def move(self) -> None:
        """Handles the ghost's resurrection after DEATH_DELAY, and
        if not frozen call find_path(), in order to move to the next square
        when self.speed has elapsed since the last move
        """
        # frozen ghost can't move
        if (self.is_frozen):
            return

        # dead ghost can rise from its ashes
        if (self.state == GhostState.DEAD
                and mlx.timer - self.last_death >= self.DEATH_DELAY):
            self.strategy = self.chase_strategy
            self.speed = self.normal_speed
            self.state = GhostState.CHASER

        if mlx.timer - self.last_s >= self.speed:
            # Targeting depends on ghost's strategy
            self.target = self.strategy.get_target(self)
            path = self.find_path((self.i, self.j), self.target)

            # Only if start≠finish (there is a cell between start and finish)
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
        """
        animates the ghost according to its state and which direction is moving
        """
        frame = "1" if (mlx.timer % 0.50 < 0.25) else "2"

        if (self.is_frozen):
            dir_ghost_key = "1white"
        elif (self.state == GhostState.CHASER):
            dir_ghost_key = f"{frame}{self.prefix}"
        elif (self.state == GhostState.FRIGHTENED):
            dir_ghost_key = f"{frame}blue"
        else:
            dir_ghost_key = "eyes"

        # displays the sprite centred on the cell
        mlx.get_tools().mlx_put_image_to_window(
            mlx.mlx_ptr,
            mlx.windows["main"],
            G_WALK_SPRITES[dir_ghost_key][self.direction],
            self.x - self.width // 2,
            self.y - self.height // 2
        )

# ===========================================================================
#                                                           FIND PATH with A*
# ===========================================================================

    def find_path(self, start: tuple[int, int],
                  goal: tuple[int, int]) -> list[tuple[int, int]]:
        """Find the shortest path from start to goal, in cells (i, j).

        Parameters
        ----------
        start: coordinates on the grid of the starting cell
        goal: coordinates on the grid of the cell to be reached

        Other variables
        ----------
        moves: 4 possible movements and bitwise value of the relevant wall
        intermediate_costs: for each cell visited,
                            the smallest number of steps found since the start
        previous_cells: for each cell, the cell we came from,
                        used to reverse path at the end.
        to_visit_heap: priority queue of cells still to be explored,
                        int: estimated total cost
                        int: cost from start to this cell
                        tuple[int, int]: this cell's coordinates
                       returns first the cell with the lowest total score.

        Returns
        ----------
        the sorted list of cells, including start and goal;
        an empty list if no path exists.
        """

        if start == goal:
            return [start]

        intermediate_costs: dict[tuple[int, int], int] = {start: 0}

        previous_cells: dict[tuple[int, int], tuple[int, int] | None] = {}
        previous_cells[start] = None

        estimated_start_to_goal = manhattan_dist(start, goal)
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

                # if accessible
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
