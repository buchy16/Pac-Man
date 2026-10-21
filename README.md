*This project has been created as part of the 42 curriculum by nbuchy and vadamavi.*

## Table of Contents

[1. Description](<#1-description>)

[2. Instructions](<#2-instructions>)

+ [3. Projet](<#3-projet>)
+ [3.1 Configuration](<#configuration>)
+ [3.2 Meilleurs scores](<#meilleurs-scores>)
+ [3.3 Génération de labyrinthe](<#génération-de-labyrinthe>)
+ [3.4 Implémentation](<#implémentation>)
+ [3.5 Architecture logicielle générale](<#architecture-logicielle-générale>)
+ [3.6 Gestion de projet](<#gestion-de-projet>)

[4. Ressources](<#4-ressources>)

+ [4.1 Références](<#références>)
+ [4.2 Usage IA](<#usage-ia>)

*[Back to top](<#table-of-contents>)*

# 1/ Description
*ToDo: présente clairement le projet, y compris son objectif et un aperçu général.*

Ce projet est inspiré de **Pac-Man**, un classique des jeux d'arcade de 1980.

Pour respecter la consigne, il a été développé en Python (3.10+), en utilisant la Programmation Orientée Objet, la bibliothèque graphique MLX et une architecture modulaire.

## Objectif
Le joueur se déplace dans un labyrinthe pour y manger toutes les Pac-gommes, tout en évitant 4 fantômes. Lorsqu'il mange une Super Pac-gomme, ce sont les fantômes devenus comestibles qui évitent Pacman pendant quelques instants.

<img src="/img/game.png" alt="Pacman game screenshot">

## Consignes principales
+ Un fichier JSON (avec commentaires) de configuration personnalisée, pour définir les paramètres du jeu.
+ Une génération de niveaux basée sur le package externe fourni "A-Maze-ing".
+ Un système de meilleurs scores persistant, par ex un fichier json sauvegardé sur le disque.
+ Une interface graphique soignée avec menu principal, vue de jeu et gestion de la fin de partie.
+ Un mode triche destiné à l'évaluation.
+ Un déploiement sur une plateforme de jeu publique, par ex Itch.io, à des fins de démonstration.

*[Back to top](<#table-of-contents>)*

# 2/ Instructions
*ToDo: toute information pertinente concernant la compilation, l'installation et/ou l'exécution.*


## Requirements

+ Python **3.10** et supérieur
+ Pour fonctionner, les packages :
	+ `commentjson`
	+ `keysymdef`
	+ `mazegenerator` (*assigned A-Maze-ing package*)
	+ `mlx`
	+ `pydantic`
+ et pour le dev :
	+ `flake8`
	+ `mypy`
	+ `pytest`


## Installation

```bash
git clone <repository-url>
cd <repository>
make install
```

## Run

The program takes **exactly one** argument, the JSON configuration file:
```bash
python3 pac-man.py config.json
```

Ou bien, pour installer et lancer le programme en une seule commande :
```bash
make
```

## Packaging

*ToDo: décrire*
+ comment recompiler le paquet :
	+ script/spec à la racine du référentiel,
	+ outil utilisé (? PyInstaller)
+ comment le mettre en ligne sur Itch.io

```bash
<packaging command>
```


## Makefile
Le projet inclut un Makefile avec les commandes imposées :
+ `install` : Installe les dépendances du projet avec le gestionnaire de paquets `uv`
+ `run` : Exécute le programme.
+ `debug` : Exécute le programme en mode debug avec `pdb`.
+ `clean` : Supprime les caches et les dossiers `build` et `dist`.
+ `lint` : Exécute
	+ `flake8 .`
	+ `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`

et la commande optionnelle :
+ `lint-strict` : Exécute `flake8 .` et `mypy . --strict`


## Game controls

| Action            | Keys                          |
| ----------------- | ----------------------------- |
| Move Pacman       | keys `W` `A` `S` `D`          |
| Pause / resume    |                               |
| Menu navigation   |                               |
| Cheat mode        |                               |


*[Back to top](<#table-of-contents>)*

# 3/ Projet

## Configuration
*ToDo: explique la structure du fichier de configuration et les valeurs par défaut.*

Le jeu est configuré via le fichier `config.json`. Les commentaires qui commencent par `#` ou `//`, full-line ou inline, sont ignorés grâce à l'utilisation de la bibliothèque `commentjson`.

### Exemple de configuration
```json
// Pac-Man settings (default values)
{
    # High scores file, must end with .json
    "highscore_filename": "highscores.json",
    # Gameplay (all optional)
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42, // seed used for first-level reproducibility
    "level_max_time": 90,
    # at least 10 levels, with unique ids between 1 and 10
    "level": [
        {"id": 1, "width": 15, "height": 15},
        {"id": 2, "width": 15, "height": 15},
        {"id": 3, "width": 15, "height": 15},
        {"id": 4, "width": 15, "height": 15},
        {"id": 5, "width": 15, "height": 15},
        {"id": 6, "width": 15, "height": 15},
        {"id": 7, "width": 15, "height": 15},
        {"id": 8, "width": 15, "height": 15},
        {"id": 9, "width": 15, "height": 15},
        {"id": 10, "width": 15, "height": 15}
    ]
}
```

#### Description des clés
| Key                       | Type     | Description                                              |
| ------------------------- | -------- | -------------------------------------------------------- |
| `highscore_filename`      | string   | File used to persist the high scores                     |
| `lives`                   | integer  | Lives at the start of a game                             |
| `pacgum`                  | integer  | ToDo: ? mandatory or not ?                               |
| `points_per_pacgum`       | integer  | Points for a pac-gum                                     |
| `points_per_super_pacgum` | integer  | Points for a super pac-gum                               |
| `points_per_ghost`        | integer  | Points for an edible ghost                               |
| `seed`                    | integer  | Seed of the first level's maze                           |
| `level_max_time`          | integer  | Time limit per level, in seconds                         |
| `level`                   | array    | List of levels, each with its own `id`, `width`, `height`|
| `level[].id`              | integer  | id of this level                                         |
| `level[].width`           | integer  | Maze width of this level                                 |
| `level[].height`          | integer  | Maze height of this level                                |


### Error handling

Un fichier de configuration défectueux ne provoque jamais de `traceback`, l'utilisateur est informé de chaque problème détecté et comment il a été géré.

Tout est journalisé avec le module `logging` configuré au niveau `INFO` dans `__main__.py` :

+ `ERROR` : le nombre d'arguments recus est différent de 1
=> le programme s'arrête avec le code de sortie `1`.
+ `WARNING` : la validation globale échoue
=> la configuration par défaut est utilisée..
+ `WARNING` : le fichier est illisible (problème d'accès ou erreur de lecture)
=> la configuration par défaut est utilisée.
+ `WARNING` : une valeur est invalide ou manquante
=> la valeur par défaut est utilisée.
+ `INFO` : une clé est inconnue
=> elle est ignorée.
+ `INFO` : une clé est manquante
=> elle est ajoutée et une valeur par défaut est utilisée.

Le module `Pydantic` gère la validation des contraintes suivantes :

+ `highscore_filename` : chaîne respectant le regex `^[a-zA-Z0-9_\-]+\.json$`
+ `lives` : entier > 0
+ `points_per_pacgum` : entier > 0
+ `points_per_super_pacgum` : entier > 0
+ `points_per_ghost` : entier > 0
+ `seed`  : entier
+ `level_max_time` : entier > 0
+ `level` : liste de 10 éléments minimum
    pour chaque élément :
    + `id` : entier, à partir de 1, non dupliqués et consécutifs
    + `width` : 3 <= entier <= 15
    + `height` : 3 <= entier <= 15

LUn exemple de journalisation et de correction d'une configuration est détaillé en annexe dans ['config.md'](/doc/config.md).

A NOTER : puisque `get_valid_config()` retourne toujours une `GameConfig` valide, le reste du jeu n'a jamais besoin de gérer une configuration incorrecte.


*[Back to top](<#table-of-contents>)*

## Meilleurs scores
*ToDo: explique le fonctionnement du système de meilleurs scores et pourquoi tu as choisi de l'implémenter ainsi.*

*[Back to top](<#table-of-contents>)*


## Génération de labyrinthe
*ToDo: explique comment le package A-Maze-ing attribué est utilisé pour générer les labyrinthes.*

Les labyrinthes sont générés par le package **A-Maze-ing**, fourni pour le projet et dont la modification n'était pas autorisée.

+ Le paramètre `PERFECT` du générateur doit impérativement être défini sur `False`, pour que les labyrinthes contiennent des boucles, afin d’obtenir des couloirs compatibles avec le jeu

+ Le niveau 1 utilise une seed fixe (`42` par défaut) ; les labyrinthes des niveaux suivants sont aléatoires.

- Un module de chargement (`<nom du module>`) adapte notre jeu à l'interface du package (et non l'inverse)..
- Le chargeur convertit la sortie du générateur (`<format : murs hexagonaux, grille, ...>`) en représentation interne sous forme de grille utilisée par le jeu (murs / couloirs, positions des pac-gums, super pac-gums aux 4 coins, apparitions des fantômes aux 4 coins, apparition du joueur au centre).

+ Si le générateur échoue (exception, sortie non valide), l’erreur est détectée et gérée correctement : `<comportement de secours>`.

*[Back to top](<#table-of-contents>)*

## Implémentation
*ToDo: résumé technique de ton implémentation.*

+ L'algorithme `A*` a été utilisé pour fournir aux fantômes le chemin le court vers leur cible, qu'il s'agisse de Pacman, d'une cible aléatoire ou d'un point de repli. Le choix de cet algorithme et son implémentation sont [détaillées ici](/doc/Astar.md)

*[Back to top](<#table-of-contents>)*

## Architecture logicielle générale
*ToDo: vue d'ensemble de haut niveau de l'architecture logicielle (modules, classes, et leurs relations).*

!! A METTRE A JOUR
```text
.
├── modules/
│   ├── mazegenerator-2.1.0-py3-none-any.whl
│   └── mlx-2.4-py3-none-any.whl
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── Mlx.py
│   ├── data/
│   │   ├── config.json
│   │   ├── parse_config.py
│   │   ├── scores.py
│   │   └── highscores.json
│   ├── game/
│   │   ├── __init__.py
│   │   ├── game.py
│   │   ├── maze.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── blinky.py
│   │   │   ├── clyde.py
│   │   │   ├── entity.py
│   │   │   ├── ghost_manager.py
│   │   │   ├── ghost.py
│   │   │   ├── inky.py
│   │   │   ├── pinky.py
│   │   │   └── player.py
│   │   └── gums/
│   │       ├── __init__.py
│   │       ├── gum.py
│   │       ├── pacgum_manager.py
│   │       ├── pacgum.py
│   │       └── super_pacgum.py
│   ├── menu/
│   │   ├── __init__.py
│   │   └── main_menu.py
│   └── utils/
│       ├── sprites.py
│       ├── directions.py
│       └── utils.py
├── assets/
│   ├── Entities/
│   │   └── ... .png
│   ├── Pacgums/
│   │   └── ... .png
│   ├── Texts/
│   │   └── ... .png
│   └── Walls/
│       └── ... .png
├── doc/
│   ├── Astar.md
│   ├── config.md
│   ├── bake_background.md
│   ├── Pacman.excalidraw
│   ├── subject_fr_v1.5.md
│   ├── todo.md
│   └── urls.md
├── tests/
│   └── test_parsing.py
├── Makefile
├── pyproject.toml
├── README.md/
└── uv.lock
```

*[Back to top](<#project-description>)*

## Gestion de projet
*ToDo: bref aperçu de la façon dont tu as géré le projet
et un lien vers le répertoire dédié à la gestion de projet.*

Au démarrage :
+ chacun a choisi les tâches sur lesquelles il souhaitait travailler ;
+ le projet a été cadré via ces 2 fichiers, qui ont ensuite été régulièrement mis à jour  :
    + [ToDo list](/doc/todo.md)
    + [Pacman.excalidraw](/doc/Pacman.excalidraw)

Le code a été partagé via github, sans conflit majeur entre les branches dédiées aux différentes fonctionalités grâce à des pull request réguliers et une communication orale le cas échéant.

Les documents de gestion du projet sont disponibles dans le répertoire dédié, [`doc/`](/doc).

*[Back to top](<#table-of-contents>)*

# 4/ Ressources

## Références
*ToDo: références classiques liées au sujet (documentation, articles, tutoriels, etc.)*

[urls partagées](/doc/urls.md)

## Usage IA
*ToDo: description de la manière dont l'IA a été utilisée : pour quelles tâches et quelles parties du projet.*

L'IA a été utilisée pour :
+ finaliser la méthode qui permet d'assembler toutes les tuiles du labyrinthe en une seule image d'arrière-plan (voir [bake_background](/doc/bake_background.md))

+ corriger des erreurs `mypy`

+ traduire ce ReadMe en anglais.

*[Back to top](<#table-of-contents>)*