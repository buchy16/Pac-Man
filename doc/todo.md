- [ ] mod op git
	+ ajouté des notes dans doc/git.md

- [ ] Itch.io
- [ ] ? musique

# Nominoé

- [x] .gitignore
- [ ] architecture modulaire et réutilisable
- [ ] joueur & pacgum
- [ ] MLX = affichage de TOUT (menu...)

# Valérie

- [x] parsing
	+ src/data/config.json
	+ src/data/parse_config.py

- [ ] highscores (recup/save)
	+ src/data/highscores
	+ src/data/scores.py !ToDo: vérif /consignes

- [ ] algos fantômes

	+ mode CHASER:
		+ Blinky chases Pac-Man
		+ Pinky targets a square four squares ahead of Pac-Man
		+ Inky moves around at random
		+ Clyde moves around at random and charges at Pac-Man when he is close
	+ mode FRIGHTENED:
		+ ~~partent tous dans le coin opposé à Pacman, at SNAIL_SPEED~~
		+ !ToDo: pour éviter la queue-leu-leu et Pacman qui se régale...
			=> revenir à l'original, chacun repart dans son coin,
			et quand arrivé dans son coin, ou si pacman se rapproche : KOI KON FAI ?
	+ mode DEAD:
		+ Returns and remains at his corner, at ROCKET_SPEED, for DEATH_DELAY

- [x] tests
	+ tests/test_parsing.py

- [ ] ReadMe
	+ en cours...
	? gif animé du jeu

# both

- [ ] répartition tâches, urls
[pytest Tutorial: Effective Python Testing – Real Python](https://realpython.com/pytest-python-testing/)

- [ ] Itch.io
- [ ] Makefile
	+ reste à faire : packaging

- [ ] ? mod op git dans doc/git.md
- [ ] ? musique
