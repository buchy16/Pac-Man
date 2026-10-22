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
		+ partent tous dans le coin opposé à Pacman, at SNAIL_SPEED
		+ !ToDo: algos différents pour éviter la queue-leu-leu et Pacman qui se régale...
	+ mode DEAD:
		+ Returns and remains at his corner, at ROCKET_SPEED, for DEATH_DELAY

- [ ] tests
	+ tests/test_parsing.py
	+ To Do or not To Do tests pour le reste du code... ?

- [ ] ReadMe
	+ en cours...

# both

- [ ] répartition tâches, urls

- [ ] Makefile
	+ reste à faire : packaging