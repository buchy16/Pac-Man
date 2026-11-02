from math import ceil
from . import Player, Ghost, Blinky, Clyde, Inky, Pinky, GhostState
from ..maze import Maze
from ...utils.directions import Direction


class GhostManager:
    """Managing movements, collisions and status of ghosts"""

    # ToDo dans '_handle_pacman_death()' :
    #   re-centrer Pacman quand il perd une vie
    #   ou gérer la fin de partie s'il n'en a plus

    def __init__(self, player: Player, maze: Maze):
        self.player = player
        self.maze = maze

        self.ghosts: dict[str, Ghost] = {
            "blinky": Blinky(self.maze, self.player,
                             "b", 1.25, 0, self.maze._width - 1, Direction.SOUTH),
            "clyde": Clyde(self.maze, self.player,
                           "c", 1.0, self.maze._height - 1, 0, Direction.NORTH),
            "inky": Inky(self.maze, self.player,
                         "i", 0.75, self.maze._height - 1, self.maze._width - 1, Direction.WEST),
            "pinky": Pinky(self.maze, self.player,
                           "p", 1.0, 0, 0, Direction.EAST),
        }

        # flag enabled/disabled when Pacman’s super-pacgum mode starts/ends
        # (to preserve the DEAD status of a ghost killed during this mode)
        self._is_superpacgum_active = False

    def _set_all_ghosts_state(self, new_state: GhostState) -> None:
        """to assign the new state to (almost) all ghosts
            when super-pacgum mode starts/ends
        """
        for ghost in self.ghosts.values():
            # a dead ghost must remain dead even if Pac-Man eats another pacgum
            if ghost.state != GhostState.DEAD:
                ghost.set_state(new_state)

    def _reset_all_ghosts(self) -> None:
        """reset ghosts on the maze"""
        for ghost in self.ghosts.values():
            ghost.i, ghost.j = ghost.i_start, ghost.j_start
            ghost.set_state(GhostState.CHASER)

    def _set_all_ghosts_freeze(self, being_frozen: bool) -> None:
        """freeze / unfreeze all ghosts"""
        for ghost in self.ghosts.values():
            ghost.is_frozen = being_frozen

    def update(self) -> None:
        """update ghosts status and handles the game logic in every frame."""

        # if Pacman has just eaten a super-pacgum
        if self.player.super_pacgum and not self._is_superpacgum_active:
            self._is_superpacgum_active = True
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

    def collision(self, name: str, hunter: Ghost) -> None:
        """Handles the collision based on the ghost's current state"""
        if hunter.state == GhostState.FRIGHTENED:
            hunter.die()
        elif hunter.state == GhostState.CHASER:
            self._handle_pacman_death(name)
        # else: ghost is DEAD, so nothing to do 

    def _handle_pacman_death(self, killer_name: str) -> None:
        """Handles Pac-Man's death for the ghosts"""
        print(f"DEBUG\t{killer_name} a tué Pacman !")

        self.player.life -= 1

        if self.player.life > 0:
            self._reset_all_ghosts()

            # ToDo: re-centrer
            self.player.i = ceil(self.maze._height / 2) - 1  # temp pour DEBUG
            self.player.j = ceil(self.maze._width / 2) - 1  # temp pour DEBUG

        else:
            # ToDo: gestion de la fin de partie par le menu
            print("DEBUG\tno more life, Pacman is dead :P")
