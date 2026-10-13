import heapq
import math
from math import ceil
from abc import abstractmethod
from enum import Enum, auto
from .entity import Entity, Direction
from .player import Player
from ..maze import Maze
from ... import mlx
from ...utils import manhattan_dist, not_closed_cell
from ...directions import DIR_MOVES
from ...sprites import G_WALK_SPRITES


class GhostState(Enum):
    CHASER = auto()       # Pursues its target (Pac-Man, random or other)
    FRIGHTENED = auto()   # Escapes from Pac-Man (far corner, random or other)
    DEAD = auto()         # Returns and remains at his corner for DEATH_DELAY


"""
4 types of ghost
    Blinky chases Pac-Man
    Pinky targets a square four squares ahead of Pac-Man
    Inky moves around at random
    Clyde moves around at random and charges at Pac-Man when he is close
"""


class Ghost(Entity):
    DEATH_DELAY: int = 10  # in seconds
    SNAIL_SPEED: int = 1.5
    ROCKET_SPEED: int = 0.15
    CORNERS: list[tuple[int, int]] = [(0,0), (0, 14), (14, 14), (14, 0)]

    def __init__(self, maze: Maze, player: Player, prefix: str, speed: float,
                 i_start: int, j_start: int, dir_start: Direction) -> None:
        """Initialize a ghost instance

        Parameters
        ----------
        maze: The maze that owns the ghost and provides tile coordinates.
        player: The player the ghost may chase.
        prefix: Sprite key, identifying this ghost's sprites.
        speed: Duration between moves, in seconds.
        i_start, j_start, dir_start: Starting row, column and direction.

        Other attributes
        ----------
        x, y: Position to display in pixels
        direction: The direction in which the ghost is heading (north, east...)
        target: Coordinates in the grid of the target cell
        state: State of the ghost (CHASER, FRIGHTENED, DEAD)
        is_frozen: To immobilise the ghost in cheat mode
        last_s: time of the last movement
        last_death: time of the last death

        """
        super().__init__(maze)
        self.player = player
        self.prefix = prefix
        self.normal_speed = speed
        self.speed = speed
        self.i_start, self.j_start = i_start, j_start
        self.direction_start = dir_start

        self.i, self.j = self.i_start, self.j_start
        self.direction = self.direction_start
        self.x, self.y = self.maze.smaze[self.i][self.j]["coor"]
        self.target: tuple[int, int]
        self.state = GhostState.CHASER
        self.is_frozen: bool = False
        self.last_s = mlx.timer
        self.last_death = 0

    def set_state(self, new_state: GhostState) -> None:
        """Allows GhostManager to change ghost's behaviour"""
        self.state = new_state
        if self.state == GhostState.FRIGHTENED:
            self.speed = self.SNAIL_SPEED
        elif self.state == GhostState.DEAD:
            self.speed = self.ROCKET_SPEED
        else:
            self.speed = self.normal_speed

    @abstractmethod
    def get_chase_target(self) -> tuple[int, int]:
        """determines the CHASER ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        pass

    def get_furthest_corner(self) -> tuple[int, int]:
        """Returns: the corner furthest from Pac-Man"""
        furthest_corner: tuple[int, int] = None
        max_distance: int = -1
        # pour chaque coin,
        for corner in self.CORNERS:
            # calculer la Distance de Manhattan
            corner_dist: int = manhattan_dist((self.player.i, self.player.j), corner)
            # si ce coin est plus loin que la distance max actuelle
            if corner_dist > max_distance:
                # mettre à jour la distance max
                max_distance = corner_dist
                # noter que ce coin est le plus éĺoigné
                furthest_corner = corner
        # return (furthest_corner)
        result = furthest_corner
        assert result in self.CORNERS, f"{result} not in {self.CORNERS}"
        return result

    def get_flee_target(self) -> tuple[int, int]:
        """determines the FRIGHTENED ghost's target on the grid
        Returns : the coordinates (i, j) of the cell to target
        """
        player_coord = (self.player.i, self.player.j)
        center_coord = (ceil(self.maze._width / 2) - 1,
                        ceil(self.maze._height / 2) - 1)
        player_to_target = manhattan_dist(player_coord, self.target)
        center_to_target = manhattan_dist(center_coord, self.target)
        # s'il a atteint sa target
        if ((self.i, self.j == self.target)
            # ou si Pacman est rentré dans le même quart que la cible
            or player_to_target < center_to_target):
            self.target = self.get_furthest_corner()
        return (self.target)

    def get_ahead_magnetic_target(self, dist: int, behind: bool = False) -> tuple[int, int]:
        """Returns:
            the further valid cell from `dist` to 0 squares ahead the player"""
        di, dj = DIR_MOVES.get(self.player.direction, (0, 0))
        max_row = self.maze._height - 1
        max_col = self.maze._width - 1

        # checks the cells from `dist` to 0 squares behind the player
        for steps in range(dist, -1, -1):
            target_row = min(max(self.player.i + di * steps, 0), max_row)
            target_col = min(max(self.player.j + dj * steps, 0), max_col)

            if not_closed_cell(self.maze, target_row, target_col):
                return (target_row, target_col)

        # when direction==NONE, `DIR_MOVES.get` returns player's position...
        # => belt, suspenders and mypy :D
        return (self.player.i, self.player.j)

    def _set_target_by_state(self) -> tuple[int, int]:
        """Points to a target algorithm depending on the state."""
        if self.state == GhostState.DEAD:
            return (self.i_start, self.j_start)
        elif self.state == GhostState.FRIGHTENED:
            # method for the FRIGHTENED mode, implemented by each ghost
            return self.get_flee_target()
        else:
            # method for the CHASER mode, implemented by each ghost
            return self.get_chase_target()

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
            self.set_state(GhostState.CHASER)

        if mlx.timer - self.last_s >= self.speed:
            # Targeting depends on ghost's state
            target_i, target_j = self._set_target_by_state()
            path = self.find_path((self.i, self.j), (target_i, target_j))

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

    def hit_player(self) -> bool:
        """
        Returns:
            True when Pac-Man and the ghost are on the same square on the grid
        """
        return (self.i == self.player.i and self.j == self.player.j)

    def die(self) -> None:
        """Changes the state of the dying ghost and starts the timer."""
        self.state = GhostState.DEAD
        self.last_death = mlx.timer

    def draw(self) -> None:
        """
        animates the ghost according to its state and which direction is moving
        """

        if (self.is_frozen):
            dir_ghost_key = "1white"

        elif (self.state == GhostState.CHASER):
            frame = "1" if (mlx.timer % 0.50 < 0.25) else "2"
            dir_ghost_key = f"{frame}{self.prefix}"

        elif (self.state == GhostState.FRIGHTENED):
            frame = "1" if (mlx.timer % 0.50 < 0.25) else "2"
            dir_ghost_key = f"{frame}blue"

        elif (self.state == GhostState.DEAD):
            dir_ghost_key = "eyes"

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
