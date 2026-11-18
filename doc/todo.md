# Last but not least

- [x] ajouter pacman.spec commente a la doc

- [ ] Supprimer `frozen=True` dans `LoadResult`

- [ ]  ~~`mypy --strict` | `mypy`: expliquer pkoi ajouter mypy.md a la doc ?~~

- [ ] si la génération d'un labyrinthe échoue,
		? gérer dans un try:
		avec un except Exception as e:
			raise Exception(f"maze generation failed: {e}")`

- [ ] verif valeurs de la config par défaut

	+ `lives`? `Game` crée `Player(self.maze)` avec les 3 vies par défaut du constructeur
	+ `highscore_filename`? `App/__init__()` crée `HighScoreStorage()` sans argument, ie chemin fixe `src/data/highscores.json`
	+ `seed` : `next_level()` passe la même `config.seed` à chaque niveau. Avec la configuration par défaut (dix niveaux de 15×15), tous les niveaux auraient donc le même labyrinthe...
	=> gênant ?
	? utiliser une graine liée au niveau (par exemple `seed + level`)
	? des dimensions différentes à chaque niveau

- [ ] ...ChassÔbugs...

- [ ] (re)norme & docstring, trad commentaires (paths.py)

- [] republier propre sur Itch.io, cpte Nominoé ?

- [ ] ReadMe
	+ finir
	? gif animé du jeu
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
