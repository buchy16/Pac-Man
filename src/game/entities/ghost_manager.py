from . import Player, Ghost, Blinky, Clyde, Inky, Pinky
from ..maze import Maze
from ...directions import Direction

"""
Excalidraw
    joueur, liste de fantômes, labyrinthe
    déplacer(), dessiner(), collision()
"""


class GhostManager():
    """Managing the movement and rendering of ghosts
    """

    def __init__(self, player: Player, maze: Maze):
        self.player = player
        self.maze = maze

        self.ghosts: dict[str, Ghost] = {
            "blinky": Blinky(self.maze, self.player, "b", 1.1, 0, 0, Direction.EAST),
            "clyde": Clyde(self.maze, self.player, "c", 1.0, 0, 14, Direction.SOUTH),
            "inky": Inky(self.maze, self.player, "i", 1.0, 14, 14, Direction.WEST),
            "pinky": Pinky(self.maze, self.player, "p", 0.8, 14, 0, Direction.NORTH),
        }

    def update(self) -> None:
        for name, ghost in self.ghosts.items():
            ghost.move()
            if ghost.hit_player():
                self.collision(name, ghost)

    def draw(self) -> None:
        for ghost in self.ghosts.values():
            ghost.draw()

    def DBG_pacman_death(self, name: str):
        print(f"DEBUG\t{name} killed Pacman!")
        for ghost in self.ghosts.values():
            ghost.i, ghost.j = ghost.i_start, ghost.j_start
        # OUCEKONGERE la mort de Pacman ?

    def collision(self, name: str, hunter: Ghost) -> None:
        if self.player.super_pacgum:
            hunter.die()
        else:
            self.DBG_pacman_death(name)
