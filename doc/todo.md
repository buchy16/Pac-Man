# Last but not least

- [ ] ...ChassÔbugs...


# Nominoé

- [ ] relire le ReadMe


`seed` : `next_level()` passe la même `config.seed` à chaque niveau.  
=> avec la configuration par défaut (dix niveaux de 15×15), tous les niveaux auraient donc le même labyrinthe...  
	=> gênant ?  
	- [ ] utiliser une graine liée au niveau (par exemple `seed + level`)  
	~~? des dimensions différentes à chaque niveau~~

- [ ] ajout sécurité en cas d'échec de la génération du labyrinthe ?  
		[genre...](<#maze-fail>)

- [ ] tester le sujet d'eval

- [x] .gitignore

- [x] architecture modulaire et réutilisable

- [x] joueur & pacgum

- [x] MLX = affichage de TOUT (menu...)

# Valérie

- [x] parsing
	+ src/data/config.json
	+ src/data/parse_config.pyBUGS CONFIG

- [x] highscores (recup/save)
	+ src/data/highscores
	+ src/data/scores.py !ToDo: vérif /consignes

- [x] algos fantômes

	+ mode CHASER:
		+ `Blinky` vise directement Pac-Man, avec `PacmanTarget` ;
		+ `Pinky` vise MAGNETIC_DISTANCE (3) cases devant Pacman, avec `NearbyTarget` ;
		+ `Inky` vise le symétrique de Blinky par rapport à MAGNETIC_DISTANCE (2) cases devant Pac-Man, avec `TrickyTarget` ;
		+ `Clyde` erre au hasard et charge quand Pac-Man se trouve à MAGNETIC_DISTANCE (3) cases ou moins, avec `RandomOrChargeTarget`.
	+ mode FRIGHTENED:
		+ choisi la case qui l'éloigne le plus de Pacman
	+ mode DEAD:
		+ Returns and remains at his corner, at ROCKET_SPEED, for DEATH_DELAY

- [x] tests
	+ tests/test_parsing.py

- [x] package PyInstaller

- [x]  valeurs de la config `lives` dans `Game` / `Player(self.maze)` 

- [x]  valeurs de la config `highscore_filename` dans `App/__init__()` / `HighScoreStorage()`  
*ooops, pas intégré dans parsing la verif d'un vrai chemin, y copris relatif à la racine du projet depuis n'importe où* :  
- [ ]  **ToDo !**


- [ ] Itch.io republier

- [ ] ReadMe mise en forme
- [ ] ReadMe verif demo en repo public
- [ ] ReadMe traduire

- [ ] A LA FIN : re-verif norme, docstring, commentaires

- [ ] tester le sujet d'eval


# both

- [x] répartition tâches, urls

- [x] Makefile, pyproject.toml



##### maze fail

*genre côté def dans `src/game/maze.py` :*
```python
from mazegenerator import MazeGenerator


class MazeGenError(Exception):
    """maze generation failure"""


class Maze(MazeGenerator):
    def __init__(self, size=(15, 15), perfect=False,
                 entry_cell=(0, 0), exit_cell=(-1, -1), seed=0) -> None:
        self._validate_params(size, entry_cell, exit_cell)
        ...
        try:
            super().__init__(size, perfect, entry_cell, exit_cell, seed)
        except Exception as err:
            raise MazeGenError(f"maze generation failed : {err}") from err
        # ? checker en + si le labyrithe est valide

    def regenerate_maze(self, size=(15, 15), perfect=False,
                        entry_cell=(0, 0), exit_cell=(-1, -1),
                        seed=0) -> None:
        ...
        try:
            self.generate(self._seed)
        except Exception as err:
            raise MazeGenError(f"maze regeneration failed : {err}") from err
        # ? checker en + si le labyrithe est valide
```

*et côté appels dans `src/game/game.py` :*
```python
from .maze import MazegenError
...
class Game(State):
	...
	def __init__(self, config: GameConfig, hight_score: HighScoreStorage) -> None:
		...
		try:
			self.maze = Maze(size=(config.level[0].width, config.level[0].height),
							 seed=config.seed)
		except (MazeGenerationError) as err:
			logging.error(f"Fatal error generating maze: {err}")
			sys.exit(1)
		...
	
	def next_level(self) -> None:
		...
		try:
		    self.maze.regenerate_maze(size=(self.config.level[self.level].width,
									  self.config.level[self.level].height),
									  seed=self.config.seed)
		except (MazeGenerationError) as err:
		    logging.error(f"Fatal error generating maze: {err}")
		    sys.exit(1)
		...
```