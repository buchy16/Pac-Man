# Last but not least

- [ ] ...ChassÔbugs...


# Nominoé

- [x] relire le ReadMe

- [x] `seed` : `next_level()` passe la même `config.seed` à chaque niveau.  
=> avec la configuration par défaut (dix niveaux de 15×15), tous les niveaux auraient donc le même labyrinthe...  
	si gênant, utiliser une graine liée au niveau (par exemple `seed + level`)

- [x] ajout sécurité en cas d'échec de la génération du labyrinthe

- [ ] derniers tests en simulant l'eval

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

- [x] valeurs de la config `lives` dans `Game` / `Player(self.maze)` 

- [x] valeurs de la config `highscore_filename` dans `App/__init__()` / `HighScoreStorage()`  

- [x] intégrer dans parsing la verif d'un chemin complet

- [x] cheat.md : mettre en foirme et preciser de figer avant skip-level

- [ ] ? modif valeurs de config.et config par défaut, pour difficulté croissante ?
- [ ] verif DEATHDELAY et autres constantes modifiées pendant les tests

- [ ] derniers tests en simulant l'eval

- [x] ReadMe mise en forme
- [x] ReadMe verif demo en repo public
- [ ] ReadMe traduire
- [ ] ? ajout freeze dans demo vidéo

- [ ] A LA FIN : re-verif norme, docstring, commentaires

- [ ] Itch.io republier


# both

- [x] répartition tâches, urls

- [x] Makefile, pyproject.toml
