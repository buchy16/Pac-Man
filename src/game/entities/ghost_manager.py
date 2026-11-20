from .player import Player
from .ghost import Ghost, GhostState
from .ghost_characters import Blinky, Clyde, Inky, Pinky
from ..maze import Maze
from ...utils.directions import Direction


class GhostManager:
    """Managing movements, collisions and status of ghosts"""

    # ToDo dans '_handle_pacman_death()' :
    #   re-centrer Pacman quand il perd une vie
    #   ou gérer la fin de partie s'il n'en a plus

    def __init__(self, player: Player, maze: Maze,
                 points_per_ghost: int) -> None:
        self.player = player
        self.maze = maze

        self.corners: list[tuple[int, int]] = [
            (0, 0),
            (0, self.maze._width - 1),
            (self.maze._height - 1, self.maze._width - 1),
            (self.maze._height - 1, 0)
        ]

        pinky = Pinky(self.maze, self.player, "p", 1.0,
                      self.corners[0], Direction.EAST)
        blinky = Blinky(self.maze, self.player, "b", 1.0,
                        self.corners[1], Direction.SOUTH)
        inky = Inky(self.maze, self.player, "i", 1.0,
                    self.corners[2], Direction.WEST)
        clyde = Clyde(self.maze, self.player, "c", 1.0,
                      self.corners[3], Direction.NORTH)

        # INJECTION DE DÉPENDANCE : fournir à Inky l'accès à l'instance blinky
        inky.set_blinky_ptr(blinky)

        self.ghosts: dict[str, Ghost] = {
            "pinky": pinky,
            "blinky": blinky,
            "inky": inky,
            "clyde": clyde,
        }

        self.points_per_ghost = points_per_ghost

        # flag enabled/disabled when Pacman’s super-pacgum mode starts/ends
        # (to preserve the DEAD status of a ghost killed during this mode)
        self._is_superpacgum_active = False

# ===========================================================================
#                                                              SET ALL GHOSTS
# ===========================================================================

    def _set_all_ghosts_state(self, new_state: GhostState) -> None:
        """to assign the new state to (almost) all ghosts
            when super-pacgum mode starts/ends
        """
        for ghost in self.ghosts.values():
            # ToDo : intégrer ici set_all_ghosts_freeze()

            # a dead ghost must remain dead even if Pac-Man eats another pacgum
            if ghost.state != GhostState.DEAD:
                # only for draw()
                ghost.state = new_state
                # for speed and strategy()
                if new_state == GhostState.FRIGHTENED:
                    ghost.strategy = ghost.flee_strategy
                    ghost.speed = ghost.SNAIL_SPEED
                elif new_state == GhostState.CHASER:
                    ghost.strategy = ghost.chase_strategy
                    ghost.speed = ghost.normal_speed

    def reset_all_ghosts(self) -> None:
        """reset ghosts on the maze"""

        self.corners = [
            (0, 0),
            (0, self.maze._width - 1),
            (self.maze._height - 1, self.maze._width - 1),
            (self.maze._height - 1, 0)
        ]

        for name, ghost in self.ghosts.items():
            ghost.reset(self.corners, name)
            ghost.reset_sliding()

        # All ghosts are CHASER again: if Pac-Man still has his super-pacgum
        # power, update() must see it as "just started" and frighten them
        # self._is_superpacgum_active = False

    # ToDo : à intégrer dans _set_all_ghosts_state()
    def set_all_ghosts_freeze(self, being_frozen: bool) -> None:
        """freeze / unfreeze all ghosts"""
        for ghost in self.ghosts.values():
            ghost.is_frozen = being_frozen

# ===========================================================================
#                                                               UPDATE & DRAW
# ===========================================================================

    def update(self) -> None:
        """update ghosts status and handles the game logic in every frame."""

        # if Pacman has just eaten a super-pacgum
        if self.player.super_pacgum and not self._is_superpacgum_active:
            self._is_superpacgum_active = True
            self._set_all_ghosts_state(GhostState.FRIGHTENED)

        # if Pacman just ate an other super-pacgum
        elif (self.player.super_pacgum
              and self.player.timer == Player.SUPER_P_TIMER):
            self._set_all_ghosts_state(GhostState.FRIGHTENED)

        # if Pacman has just lost the super-pacgum power
        elif not self.player.super_pacgum and self._is_superpacgum_active:
            self._is_superpacgum_active = False
            self._set_all_ghosts_state(GhostState.CHASER)

        # Since the ghosts are in the right state, they can move
        for name, ghost in self.ghosts.items():
            ghost.move()
            if ghost.hit_player():
                self.collision(name, ghost)

    def draw(self) -> None:
        for ghost in self.ghosts.values():
            ghost.draw()

# ===========================================================================
#                                                            PACMAN COLLISION
# ===========================================================================

    def collision(self, name: str, hunter: Ghost) -> None:
        """Handles the collision based on the ghost's current state"""
        if hunter.state == GhostState.FRIGHTENED:
            hunter.die()
            self.player.score += self.points_per_ghost
        elif hunter.state == GhostState.CHASER:
            self._handle_pacman_death(name)
        # else: ghost is DEAD, so nothing to do

    def _handle_pacman_death(self, killer_name: str) -> None:
        """Handles Pac-Man's death for the ghosts"""
        print(f"DEBUG\t{killer_name} a tué Pacman !")

        self.player.player_hit()

        if self.player.life > 0:
            self.reset_all_ghosts()

        else:
            # ToDo: gestion de la fin de partie par le menu
            print("DEBUG\tno more life, Pacman is dead :P")
