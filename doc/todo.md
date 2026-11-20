# Last but not least

- [x] ajouter pacman.spec commente a la doc

- [ ] Supprimer `frozen=True` dans `LoadResult`  
		*ah oui pour la logique... mais non pour mypy*

- [ ]  `mypy --strict` | `mypy`: expliquer pkoi ajouter mypy.md a la doc ?  
		*ben finalement le strict marche si on ajoute un stub :D*

- [ ] Pas de sécurité en cas d'échec de la génération du labyrinthe ?  [genre...](<#maze-fail>)

verifs valeurs de la config par défaut :  
- [ ]  `lives`? `Game` crée `Player(self.maze)` avec les 3 vies par défaut du constructeur
- [ ]  `highscore_filename`? `App/__init__()` crée `HighScoreStorage()` sans argument, ie chemin fixe `src/data/highscores.json`  
		*ooops, pas intégré dans parsing la verif d'un vrai chemin, y copris relatif à la racine du projet depuis n'importe où*
		=> **ToDo !**


- [ ]  `seed` : `next_level()` passe la même `config.seed` à chaque niveau. Avec la configuration par défaut (dix niveaux de 15×15), tous les niveaux auraient donc le même labyrinthe...  
	=> gênant ?  
	? utiliser une graine liée au niveau (par exemple `seed + level`)  
	? des dimensions différentes à chaque niveau

- [ ] ...ChassÔbugs...

- [ ] (re)norme & docstring, trad commentaires
	- [x] paths.py

- [ ] republier propre sur Itch.io, cpte Nominoé ?

- [ ] ReadMe
	+ finir
	+ ? gif animé du jeu
	+ traduire


# Nominoé

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

- [] package
	+ OK PyInstaller
	+ Itch.io à mettre à jour qd fini

- [ ] ReadMe
	+ en cours...
	? gif animé du jeu


# both

- [x] répartition tâches, urls

- [x] Makefile, pyproject.toml

- [ ] ? musique



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