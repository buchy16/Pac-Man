# Pacman

## Fantômes ! Encore des fantômes !

*Résumé : Recrée le célèbre jeu d'arcade Pac-Man !*

*Version : 1.5*

---

## Table des matières

- **I** Avant-propos ......................................................... 2
- **II** Instructions IA ...................................................... 3
- **III** Instructions communes ............................................... 5
  - III.1 Règles générales .................................................. 5
  - III.2 Makefile .......................................................... 5
  - III.3 Consignes supplémentaires ......................................... 6
- **IV** Partie obligatoire ................................................... 7
- **V** Spécifications détaillées ............................................. 8
  - V.1 Utilisation ......................................................... 8
  - V.2 Fichier de configuration ............................................ 8
  - V.3 Gestion d'une configuration erronée ................................. 9
  - V.4 Intégration du générateur de labyrinthe ............................. 9
  - V.5 Système de meilleurs scores ......................................... 9
- **VI** Spécifications du jeu ............................................... 11
  - VI.1 Structure d'un niveau ............................................. 11
  - VI.2 Joueur ............................................................ 12
  - VI.3 Fantômes .......................................................... 12
  - VI.4 Pac-gommes et Super-pac-gommes .................................... 12
  - VI.5 Mode triche ....................................................... 13
  - VI.6 Score .............................................................. 14
  - VI.7 Progression du jeu ................................................ 14
  - VI.8 Interface utilisateur ............................................. 15
- **VII** Packaging du projet ................................................ 16
- **VIII** Gestion de projet ................................................. 17
- **IX** Exigences du README ................................................ 18
- **X** Rendu et correction par les pairs .................................... 20

---

## Chapitre I — Avant-propos

Sorti pour la première fois en 1980 par Namco, **Pac-Man** est rapidement devenu une icône culturelle et l'un des jeux vidéo les plus influents de tous les temps. Conçu par Toru Iwatani, son objectif était de créer un jeu capable de séduire les femmes et les joueurs occasionnels, en rupture avec les jeux de tir spatiaux de l'époque. Le jeu a introduit l'IA des fantômes, désormais célèbre, chacun ayant un comportement unique (Blinky poursuit, Pinky tend des embuscades, Inky est imprévisible, et Clyde est... bizarre).

Pac-Man a également été le premier jeu à populariser le concept de power-up — la Pac-gomme (ou Power Pellet) qui permet de manger les fantômes. La machine d'arcade originale comptait 256 niveaux, mais en raison d'un bug de dépassement d'entier, le niveau 256 était impossible à terminer, ce que l'on appelle le fameux « kill screen ».

Avec ce projet, tu vas redonner vie à ce classique en construisant ta propre version — en Python, avec une structure moderne et une organisation de projet, prête à être déployée sur une véritable plateforme de jeu. Waka-waka !

---

## Chapitre II — Instructions IA

### ● Contexte

Au cours de ton parcours d'apprentissage, l'IA peut t'aider dans de nombreuses tâches différentes. Prends le temps d'explorer les différentes capacités des outils IA et la façon dont ils peuvent soutenir ton travail. Cependant, aborde-les toujours avec prudence et évalue leurs résultats de manière critique. Qu'il s'agisse de code, de documentation, d'idées ou d'explications techniques, tu ne peux jamais être totalement certain que ta question était bien formulée ou que le contenu généré est exact. Tes pairs sont une ressource précieuse pour t'aider à éviter les erreurs et les angles morts.

### ● Message principal

- ☛ Utilise l'IA pour réduire les tâches répétitives ou fastidieuses.
- ☛ Développe des compétences de prompting — aussi bien pour le code que hors code — qui te seront utiles dans ta future carrière.
- ☛ Apprends comment fonctionnent les systèmes d'IA afin de mieux anticiper et éviter les risques, biais et problèmes éthiques courants.
- ☛ Continue à développer tes compétences techniques et humaines en travaillant avec tes pairs.
- ☛ N'utilise que du contenu généré par l'IA que tu comprends entièrement et dont tu peux assumer la responsabilité.

### ● Règles pour l'apprenant :

- Tu dois prendre le temps d'explorer les outils IA et de comprendre leur fonctionnement, afin de les utiliser de manière éthique et de réduire les biais potentiels.
- Tu dois réfléchir à ton problème avant de prompter — cela t'aide à écrire des prompts plus clairs, plus détaillés et plus pertinents, en utilisant un vocabulaire précis.
- Tu dois prendre l'habitude de vérifier, revoir, questionner et tester systématiquement tout ce qui est généré par l'IA.
- Tu dois toujours rechercher une relecture par les pairs — ne te fie pas uniquement à ta propre validation.

### ● Résultats attendus de cette phase :

- Développer des compétences de prompting à la fois générales et spécifiques au domaine.
- Améliorer ta productivité grâce à une utilisation efficace des outils IA.
- Continuer à renforcer la pensée computationnelle, la résolution de problèmes, l'adaptabilité et la collaboration.

### ● Commentaires et exemples :

- Tu rencontreras régulièrement des situations — examens, évaluations, et autres — où tu devras démontrer une réelle compréhension. Sois préparé, continue à développer tes compétences techniques et interpersonnelles.
- Expliquer ton raisonnement et débattre avec tes pairs révèle souvent des lacunes dans ta compréhension. Fais de l'apprentissage entre pairs une priorité.
- Les outils IA manquent souvent de ton contexte spécifique et ont tendance à fournir des réponses génériques. Tes pairs, qui partagent ton environnement, peuvent offrir des perspectives plus pertinentes et précises.
- Là où l'IA a tendance à générer la réponse la plus probable, tes pairs peuvent apporter des points de vue alternatifs et des nuances précieuses. Appuie-toi sur eux comme point de contrôle qualité.

**✓ Bonne pratique :**

> Je demande à l'IA : « Comment tester une fonction de tri ? » Elle me donne quelques idées. Je les essaie et je passe en revue les résultats avec un pair. Nous affinons l'approche ensemble.

**✗ Mauvaise pratique :**

> Je demande à l'IA d'écrire une fonction entière, je la copie-colle dans mon projet. Lors de l'évaluation par les pairs, je suis incapable d'expliquer ce qu'elle fait ni pourquoi. Je perds ma crédibilité — et j'échoue à mon projet.

**✓ Bonne pratique :**

> J'utilise l'IA pour m'aider à concevoir un parseur. Puis je passe en revue la logique avec un pair. Nous trouvons deux bugs et le réécrivons ensemble — en mieux, plus proprement, et en comprenant tout parfaitement.

**✗ Mauvaise pratique :**

> Je laisse Copilot générer le code d'une partie clé de mon projet. Il compile, mais je ne peux pas expliquer comment il gère les pipes. Lors de l'évaluation, je n'arrive pas à le justifier et j'échoue à mon projet.

---

## Chapitre III — Instructions communes

### III.1 Règles générales

- Ton projet doit être écrit en **Python 3.10 ou une version ultérieure**.
- Ton projet doit respecter la norme de codage **flake8**.
- Tes fonctions doivent gérer les exceptions correctement afin d'éviter tout crash. Utilise des blocs try-except pour gérer les erreurs potentielles. Privilégie les gestionnaires de contexte pour les ressources telles que les fichiers ou les connexions, afin d'assurer un nettoyage automatique. Si ton programme plante à cause d'exceptions non gérées lors de la correction, il sera considéré comme non fonctionnel.
- Toutes les ressources (par exemple, descripteurs de fichiers, connexions réseau) doivent être correctement gérées pour éviter les fuites. Utilise des gestionnaires de contexte autant que possible pour une gestion automatique.
- Ton code doit inclure des annotations de type pour les paramètres de fonctions, les types de retour et les variables lorsque cela s'applique (en utilisant le module `typing`). Utilise mypy pour la vérification statique des types. Toutes les fonctions doivent passer mypy sans erreur.
- Inclue des docstrings dans les fonctions et les classes, en suivant la PEP 257 (par exemple, style Google ou NumPy) pour documenter l'objectif, les paramètres et les valeurs de retour.

### III.2 Makefile

Inclue un `Makefile` dans ton projet pour automatiser les tâches courantes. Il doit contenir les règles suivantes (le lint obligatoire implique les options spécifiées ; il est fortement recommandé d'essayer `-strict` pour une vérification renforcée) :

- **install** : Installer les dépendances du projet en utilisant pip, uv, pipx, ou tout autre gestionnaire de paquets de ton choix.
- **run** : Exécuter le script principal de ton projet (par exemple, via l'interpréteur Python).
- **debug** : Exécuter le script principal en mode debug en utilisant le débogueur intégré de Python (par exemple, pdb).
- **clean** : Supprimer les fichiers temporaires ou les caches (par exemple, `__pycache__`, `.mypy_cache`) afin de garder l'environnement du projet propre.
- **lint** : Exécuter les commandes `flake8 .` et `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`
- **lint-strict** (optionnel) : Exécuter les commandes `flake8 .` et `mypy . --strict`

### III.3 Consignes supplémentaires

- Crée des programmes de test pour vérifier le bon fonctionnement du projet (non soumis ni noté). Utilise des frameworks comme pytest ou unittest pour les tests unitaires, en couvrant les cas limites.
- Inclue un fichier `.gitignore` pour exclure les artefacts Python.
- Il est recommandé d'utiliser des environnements virtuels (par exemple, venv ou conda) pour isoler les dépendances pendant le développement.

*Si des exigences supplémentaires spécifiques au projet s'appliquent, elles seront indiquées immédiatement après cette section.*

---

## Chapitre IV — Partie obligatoire

Dans ce projet, tu vas créer un jeu **Pac-Man** complet et jouable en Python, en utilisant la programmation orientée objet, une bibliothèque graphique simple (MLX ou équivalente), et une architecture modulaire et réutilisable.

> **ℹ️** Une bibliothèque graphique est considérée comme *similaire à MLX* si chaque fonction que tu utilises a un équivalent dans la bibliothèque MLX. Si une fonction dont tu dépends n'a pas d'équivalent MLX, elle n'est pas autorisée.

Le jeu doit prendre en charge :

- Une configuration personnalisée via un fichier (JSON avec commentaires) pour définir les paramètres du jeu.
- Une gestion robuste des erreurs, aucun crash !
- Une génération de niveaux basée sur un package externe « A-Maze-ing » (pas le tien !).
- Un système de meilleurs scores persistant, au choix (stocké dans un fichier json dans le projet, sauvegardé sur le disque, etc.).
- Une interface graphique soignée avec menu principal, vue de jeu et gestion de la fin de partie.
- Un mode triche destiné à l'évaluation.
- Un déploiement sur une plateforme de jeu publique (Steam/Itch.io ou équivalente) à des fins de démonstration.

Une attention particulière sera portée à la gestion de projet, et plusieurs documents seront demandés.

### Boucle de jeu

- Menu principal > démarrer une partie > Victoire ou Défaite > Saisir un nom pour le meilleur score > Retour au menu principal

---

## Chapitre V — Spécifications détaillées

### V.1 Utilisation

Ton programme doit être lancé depuis la ligne de commande comme suit :

```
$> python3 pac-man.py config.json
```

- Il doit prendre **exactement un** argument : un fichier de configuration. Le nom du fichier n'a pas d'importance, mais le fichier doit être un fichier json.
- Toute erreur (fichier manquant, valeur invalide, clé manquante) doit être gérée proprement avec des messages clairs, **jamais** avec une trace Python (traceback).

### V.2 Fichier de configuration

Le fichier de configuration utilise le format JSON. En plus du format JSON standard, tu dois gérer les commentaires. Les lignes commençant par `#` sont des commentaires et doivent être ignorées. Tu peux également prendre en charge d'autres styles de commentaires (par exemple, style C ou C++).
La structure exacte est libre, mais documente tes clés dans le README et prévois des valeurs par défaut robustes.

Clés suggérées (les noms sont indicatifs) :

- `highscore_filename`
- `level` tableau de plusieurs niveaux
- `width`, `height` pour chaque niveau
- `lives` : 3
- `pacgum` : 42
- `points_per_pacgum` : 10
- `points_per_super_pacgum` : 50
- `points_per_ghost` : 200
- `seed` : 42
- `level_max_time` : 90

### V.3 Gestion d'une configuration erronée

En cas de valeurs manquantes ou invalides, reviens à des valeurs par défaut sûres, enregistre un message clair, et continue. Les clés inconnues doivent être ignorées. Aucune trace (traceback).

> **⚠️** La configuration du jeu sera modifiée lors de la soutenance.

### V.4 Intégration du générateur de labyrinthe

Tu **ne dois pas** écrire ton propre générateur.
Au démarrage du projet, un package *A-Maze-ing* réalisé par un autre groupe te sera attribué :

- Tu dois utiliser leur package **tel quel**, sans le modifier. Le package attribué sera réinstallé lors de ta correction par les pairs.
- Ton loader doit s'adapter à leur interface, et non l'inverse.
- Le paramètre `PERFECT` sera fixé à `False` pour produire des couloirs compatibles avec Pac-Man (voir le sujet A-Maze-ing).
- Si le générateur échoue, tu dois gérer l'erreur proprement.

### V.5 Système de meilleurs scores

Tu dois implémenter un système de meilleurs scores persistant.
L'implémentation exacte est libre, mais documente-la dans le README.

Il doit :

- Être stocké comme tu le souhaites (par exemple, fichier json dans le projet, sur le disque, etc.).
- Être robuste face aux erreurs de fichier (fichier manquant, format invalide, etc.).
- Gérer les noms de joueurs (10 caractères maximum, alphanumériques et espaces uniquement).
- Gérer les scores (entiers non négatifs).
- Conserver les 10 meilleurs scores, avec noms des joueurs et scores.
- Charger les meilleurs scores au démarrage du jeu et les sauvegarder à la fin de la partie.
- Permettre aux joueurs de saisir leur nom à la fin de la partie (victoire ou défaite).
- Afficher les meilleurs scores dans le menu principal.

---

## Chapitre VI — Spécifications du jeu

### VI.1 Structure d'un niveau

- Un labyrinthe avec des murs et des couloirs, généré par le package A-Maze-ing attribué.
- Le premier niveau est composé d'un labyrinthe généré avec une seed fixe (par exemple, 42), puis chaque niveau suivant est composé d'un labyrinthe généré aléatoirement.
- Des pac-gommes (petits points) dans la plupart des couloirs.
- Des super-pac-gommes (power pellets) dans les 4 coins du labyrinthe.
- 4 fantômes, un dans chaque coin du labyrinthe.
- Le joueur démarre au centre du labyrinthe.

### VI.2 Joueur

- Peut se déplacer uniquement dans les couloirs (pas dans les murs).
- Peut se déplacer dans 4 directions (haut, bas, gauche, droite) en utilisant les flèches directionnelles ou WASD (selon ton clavier).
- Commence avec 3 vies.
- Perd une vie lorsqu'il est touché par un fantôme.
- Réapparaît au centre du labyrinthe après avoir perdu une vie.
- Fin de partie lorsque toutes les vies sont perdues.
- Gagne le niveau lorsque toutes les pac-gommes sont mangées.
- Gagne la partie lorsque tous les niveaux sont terminés.
- Manger une pac-gomme augmente le score de X points.
- Manger une super-pac-gomme (power pellet) augmente le score de Y points et rend les fantômes comestibles pendant un court instant.
- Manger un fantôme comestible augmente le score de Z points.

### VI.3 Fantômes

- Se déplacent de manière autonome dans les couloirs.
- Poursuivent le joueur lorsqu'ils ne sont pas comestibles. C'est à toi de définir le comportement de poursuite (basé sur la distance, aléatoire, etc.).
- Fuient le joueur lorsqu'ils sont comestibles.
- Réapparaissent dans leur coin après un certain délai lorsqu'ils sont mangés (par exemple, après 5 ou 10 secondes).

### VI.4 Pac-gommes et Super-pac-gommes

- Les pac-gommes sont de petits points placés dans la plupart des couloirs.
- Les super-pac-gommes (power pellets) sont des points plus gros placés dans les 4 coins du labyrinthe.
- Manger une pac-gomme augmente le score de X points.
- Manger une super-pac-gomme augmente le score de Y points et rend les fantômes comestibles pendant un court instant.

### VI.5 Mode triche

- Peut être activé pour faciliter la correction par les pairs.
- Fonctionnalités suggérées :
  - Invincibilité (aucune vie perdue ; les fantômes ne peuvent pas manger le joueur).
  - Passage de niveau (remporter immédiatement le niveau en cours).
  - Gel des fantômes (les fantômes arrêtent de bouger).
  - Vies supplémentaires (ajouter des vies supplémentaires au joueur).
  - Vitesse augmentée (le joueur se déplace plus vite).
  - Toute autre fonctionnalité qui pourrait être utile.

Garde à l'esprit que le mode triche est destiné à la correction par les pairs, et qu'il doit donc réellement aider le correcteur à tester facilement toutes les fonctionnalités de ton jeu.

### VI.6 Score

- Le score augmente lorsque :
  - On mange une pac-gomme (+X points).
  - On mange une super-pac-gomme (+Y points).
  - On mange un fantôme comestible (+Z points).
- Le score ne diminue jamais.

### VI.7 Progression du jeu

- Le jeu est composé de plusieurs niveaux (au moins 10).
- Chaque niveau a une limite de temps (par exemple, 90 secondes).
- Si la limite de temps est atteinte, c'est à toi de décider de ce qui se passe (par exemple, redémarrer le niveau, terminer la partie, etc.).
- Si le joueur termine un niveau, il passe au niveau suivant.
- Le joueur conserve son score et ses vies restantes entre les niveaux.
- La partie se termine lorsque tous les niveaux sont terminés ou lorsque le joueur perd toutes ses vies.
- Pendant la partie, le joueur peut mettre en pause et reprendre le jeu.
- Lorsque la partie se termine (victoire ou défaite), le score final est affiché, et le joueur peut saisir son nom pour enregistrer son meilleur score.
- Après la fin de la partie, le joueur retourne au menu principal.

### VI.8 Interface utilisateur

- **Menu principal :**
  - Démarrer une partie — Permet au joueur de commencer une nouvelle partie.
  - Voir les meilleurs scores — Affiche le **Top 10** des scores avec les noms des joueurs.
  - Instructions — Affiche les contrôles et les règles du jeu.
  - Quitter — Ferme l'application du jeu.
- **HUD en jeu (toujours visible pendant la partie) :**
  - Score actuel
  - Vies restantes
  - Niveau actuel
  - Temps restant pour le niveau
- **Menu pause :**
  - Reprendre la partie — Permet au joueur de revenir à la partie en cours.
  - Retourner au menu principal — Permet au joueur de quitter la partie en cours et de retourner au menu principal.
- **Écran de fin de partie :**
  - Affiche le score final.
  - Invite le joueur à saisir son nom pour enregistrer son score dans la liste des meilleurs scores.
- **Écran de victoire :**
  - Affiche le score final et un message de félicitations.
  - Invite le joueur à saisir son nom pour enregistrer son score dans la liste des meilleurs scores.

---

## Chapitre VII — Packaging du projet

Tu dois livrer :

- Un jeu complet pouvant être installé et lancé depuis une plateforme publique (par exemple, Steam ou Itch.io) sous forme de build gratuit mais non répertorié/privé.
- Le jeu packagé doit être pleinement fonctionnel.
- Fournir des instructions minimales dans le package (contrôles, options, configuration).
- Ton dépôt Git doit contenir l'intégralité du code source ainsi que le script/la spec de packaging à la racine.
- Il est possible qu'on te demande de régénérer le package lors de la correction par les pairs.

---

## Chapitre VIII — Gestion de projet

Au cours de ce projet, tu dois utiliser une approche structurée pour piloter le projet et en fournir des preuves. Tu es libre d'utiliser toute approche et tout outil dont tu pourrais avoir besoin pour soutenir la gestion de ton projet. Tu dois produire différents documents prouvant ton approche.
Dans un sous-répertoire dédié de ton dépôt, inclue tous les éléments pertinents.

Exemples :

- Planning de projet, Gantt, Kanban, etc.
- Suivi réel de l'avancement, comparé au planning.
- Analyse du projet, et choix associés.
- Analyse des risques, et mesures d'atténuation possibles.
- Organisation de l'équipe (qui a fait quoi, comment les décisions ont été prises, comment les problèmes ont été gérés).
- Plan de tests de recette (fonctionnalités testées, bugs trouvés/corrigés).
- Résumé des points de blocage ou conflits survenus pendant le projet.
- etc.

---

## Chapitre IX — Exigences du README

Un fichier `README.md` doit être fourni à la racine de ton dépôt Git. Son but est de permettre à toute personne ne connaissant pas le projet (pairs, staff, recruteurs, etc.) de comprendre rapidement de quoi il s'agit, comment l'exécuter, et où trouver davantage d'informations sur le sujet.

Le `README.md` doit inclure au minimum :

- La toute première ligne doit être en italique et se lire : *Ce projet a été créé dans le cadre du cursus 42 par \<login1\>[, \<login2\>[, \<login3\>[...]]].*
- Une section « **Description** » qui présente clairement le projet, y compris son objectif et un aperçu général.
- Une section « **Instructions** » contenant toute information pertinente concernant la compilation, l'installation et/ou l'exécution.
- Une section « **Ressources** » listant les références classiques liées au sujet (documentation, articles, tutoriels, etc.), ainsi qu'une description de la manière dont l'IA a été utilisée — en précisant pour quelles tâches et quelles parties du projet.

> ➠ **Des sections supplémentaires peuvent être exigées selon le projet** (par exemple, exemples d'utilisation, liste des fonctionnalités, choix techniques, etc.).

*Tout ajout requis sera explicitement listé ci-dessous.*

- Une section **Configuration** expliquant la structure du fichier de configuration et les valeurs par défaut.
- Une section **Meilleurs scores** expliquant le fonctionnement du système de meilleurs scores et pourquoi tu as choisi de l'implémenter ainsi.
- Une section **Génération de labyrinthe** expliquant comment le package A-Maze-ing attribué est utilisé pour générer les labyrinthes.
- Une section **Implémentation** avec un résumé technique de ton implémentation.
- Une section **Architecture logicielle générale**, avec une vue d'ensemble de haut niveau de l'architecture logicielle (modules, classes, et leurs relations).
- Une section **Gestion de projet**, avec un bref aperçu de la façon dont tu as géré le projet et un lien vers le répertoire dédié à la gestion de projet.

> **ℹ️** Ton README doit être rédigé en anglais.

---

## Chapitre X — Rendu et correction par les pairs

Soumets ton travail dans ton dépôt Git comme d'habitude. Seul le contenu de ton dépôt sera examiné lors de la soutenance. N'hésite pas à vérifier à nouveau les noms de tes fichiers pour t'assurer qu'ils sont corrects.

### Instructions de recodage

Lors de l'évaluation, une brève **modification du projet** peut occasionnellement être demandée. Cela peut impliquer un léger changement de comportement, quelques lignes de code à écrire ou réécrire, ou une fonctionnalité facile à ajouter.

Bien que cette étape ne soit **pas nécessairement applicable à tous les projets**, tu dois t'y préparer si elle est mentionnée dans les consignes d'évaluation.

Cette étape vise à vérifier ta compréhension réelle d'une partie spécifique du projet. La modification peut être réalisée dans l'environnement de développement de ton choix (par exemple, ton installation habituelle), et devrait être réalisable en quelques minutes — sauf si un délai spécifique est défini dans le cadre de l'évaluation.
On peut par exemple te demander de mettre à jour légèrement une fonction ou un script, de modifier un affichage, ou d'ajuster une structure de données pour stocker de nouvelles informations, etc.

Les détails (portée, cible, etc.) seront précisés dans les **consignes d'évaluation** et peuvent varier d'une évaluation à l'autre pour un même projet.