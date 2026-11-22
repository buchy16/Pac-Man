Ce planning reflète l'avancement réel du projet : au démarrage aucune échéance précise n'avait été fixée car l'un des binômes devait travailler en parallèle sur un autre projet.

Une 1ère répartition des tâches a simplement été effectuée, cf [repartition_taches.md](project_management/repartition_taches.md).


# Jalons du projet

## Cadrage & socle technique (17–23 sept)

Poser le dépôt, outiller le projet, comprendre la MinilibX :

- Initial commit
- 1er schéma d’architecture sur Excalidraw
- Structure de la documentation (todo, README, sujet, liens)
- Makefile organisé par groupes de dépendances
- Parsing
- Prise en main de la MinilibX, classe wrapper de la MLX pour structurer le code
- premiers assets (murs), classe `Maze` avec affichage

## Rendu, joueur, menu & gommes (24 sept–2 oct)

Obtenir un premier jeu jouable et navigable :

- Tests unitaires parsing/models
- Labyrinthe enrichi et tuiles agrandies
- Squelette des entités ; Déplacement joueur, animations, coordonnées graphiques, centralisation des sprites
- Pacgums et super-pacgums avec affichage et score
- Menu fonctionnel et page d’instructions
- Gestion des highscores en version bêta

## Fantômes (6–14 oct)

Donner des adversaires au joueur :

- Correction d’un import circulaire ;
- Sprites, états des fantômes ; Début des collisions avec Pac-Man, comportement de fuite
- Menu pause et refonte du passage menu ↔ jeu

## HUD & Conformité (19–23 oct)

Aligner le code sur le sujet, réorganiser :

- Refonte du parsing pour suivre strictement le sujet ; Tests unitaires v2
- Réorganisation des dossiers ; 1er passage flake8 et mypy ; docs A\* et config ;
- HUD : vies, niveau, timer ; retour au menu en fin de partie, game over

## Pause (24 oct - 1 nov)

Congés pendant les vacances de la Toussaint :D

## Boucle de jeu complète (2–7 nov)

Fermer la boucle de jeu et enrichir le gameplay :

- Refonte des fantômes avec stratégies de ciblage
- Boucle mort/victoire ; correction des timers du super-pacgum (PR #15, #16)
- Mode cheats
- HUD refondu en classe
- Déplacements fluides de Pac-Man et des fantômes

## Finitions & packaging 9–16 nov

Stabiliser, nettoyer, rendre le jeu distribuable :

- Affichage de texte et scores, écrans de victoire/défaite
- Libération des assets en fin de programme
- Modification de la fuite des fantômes ; correction de l’état « effrayé » après résurrection
- Mise à la norme
- Packaging avec PyInstaller

## Documentation & livraison (20–21 nov)

Rendre le projet présentable et transmissible :

- Derniers réglages
- Mise à jour du README et de la doc, mini démo vidéo