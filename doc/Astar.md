L'algorithme `A*` a été utilisé pour fournir aux fantômes le chemin le court vers leur cible, qu'il s'agisse de Pacman, d'une cible aléatoire ou d'un point de repli.

## BFS / A*
Ces deux algorithmes garantissent mathématiquement de trouver le chemin optimal, mais `A*` est en quelque sorte un `BFS` amélioré.

### BFS
Le **BFS est "*aveugle*"**, il s'étale sur la zone à explorer comme une tache d'huile, dans TOUTES les directions possibles :
* Il explore les 4 cases à distance 1 du départ (Nord, Sud, Est, Ouest) ;
* puis toutes les cases à distance 2 ;
* puis toutes les cases distance 3 ;
* etc.
Donc il **perd du temps** à explorer des couloirs qui partent dans la direction opposée de la cible.


### A*
**A* utilise une *"boussole"***, il calcule un coût pour chaque case voisine à visiter et explore celle qui a le coût le plus faible.

Ce coût `f(Case_n)` est une estimation de la distance totale à parcourir, pour aller du départ `Case_start` à l'arrivée `Case_end` en passant par `Case_n` :

On le calcule avec `f(Case_n) = g(Case_n) + h(Case_n)` :

+ `g(Case_n)` est le coût réel depuis `Case_start` jusque `Case_n`
  = le nombre exact, et minimum, de cases franchies depuis le départ pour arriver jusque là.

+ `h(Case_n)` est une évaluation heuristique du coût  depuis `Case_n` jusque `Case_end`
  = estimation de la distance restante entre cette case et la cible.

En explorant prioritairement la case au coût le plus faible, `A*` visite **en priorité les cases les plus prometteuses**.

### Distance de Manhattan

Manhattan ressemble à un labyrinthe 2D sans diagonales :
+ impossible d'aller tout droit (*distance euclidienne*) à travers les immeubles,
+ il faut marcher le long des rues (*distance de Manhattan*) pour aller d'un point $A(i_1, j_1)$ à un point $B(i_2, j_2)$.

La distance de Manhattan  $\text{distance} = \vert{}i_1 - i_2\vert{} + \vert{}j_1 - j_2\vert{}$ est utilisée pour l'évaluation heuristique du `A*` car :
+ elle est extrêmement rapide à calculer ;
+ elle ne surestime jamais la distance réelle.

Exemple de calcul, entre deux cases `A(2,3)` et `B(5,7)` :
	$\vert{}2 - 5\vert{} + \vert{}3 - 7\vert{} = 3 + 4 = 7$ cases d'écart minimum.

## Implémentation

### Structures utilisées pour explorer le labyrinthe

#### `intermediate_costs`
Un **dictionnaire pour stocker les valeurs** `g(Case_n)` : `intermediate_costs: dict[tuple[int, int], int]`

Il contient pour chaque cellule découverte :
+ ses coordonnées
+ le nombre minimum de cases parcourues pour l'atteindre depuis la case de départ

#### `previous_cells`
Un **dictionnaire pour reconstituer le chemin le plus court** : `previous_cells: dict[tuple[int, int], tuple[int, int] | None]`

Ses clés constituent aussi l'ensemble des cellules découvertes, il contient pour chaque cellule explorée :
+ ses coordonnées
+ les coordonnées de la case précédente sur le meilleur chemin connu

#### `to_visit_heap`
Une **file d’attente** qui sort toujours en priorité la case avec le plus petit coût total : `to_visit_heap: list[tuple[int, int, tuple[int, int]]]`

Cette liste utilise le module `heapq` de Python qui fournit un tas min capable 
+ quel que soit l'ordre dans lequel les éléments ont été ajoutés,
+ sans jamais avoir besoin de trier toute la liste,

de :
+ sortir toujours l'élément le plus prioritaire ;
+ ajouter des éléments avec `heappush()`; 
+ retirer le plus petit  avec `heappop()`.
	*(la liste n'est pas triée, seul `tas[0]` est garanti d'être le plus petit)*

On stocke donc dans `to_visit_heap` des triplets `(f(Case_n), g(Case_n), coord_Case_n)]` :
+ `f(Case_n)` = *estimation de la distance totale*
+ `g(Case_n)` = *coût réel depuis `Case_start` jusque `Case_n`*
+ coord_Case_n = *coordonnées de `Case_n`*
et ces triplets seront triés d'abord par coût total, puis par coût intermédiaire réel.

**A noter** que cette liste peut contenir plusieurs entrées pour une même case, donc AVANT de l'ajouter à `intermediate_costs` il faudra vérifier qu'elle n'y figure pas déjà avec un son coût `g()` inférieur. C'est plus économique d'avoir des entrées périmées dans le tas et de les écarter au moment où elles sortent, car supprimer ou modifier un élément quelconque du tas se ferait avec un coût en O(n).

### Algorithme

1. on commence par la case de départ `Case_start`
	+ on l'ajoute au dictionnaire des cases découvertes, avec son coût `g()` : `intermediate_costs = {start: 0}`
	+ on l'ajoute au dictionnaire des cases précédentes, sans antécédent : `previous_cells[start] = None`
	+ on l'ajoute à la liste des cases à explorer, avec ses coûts `f() `et `g()` : `to_visit_heap = [(manhattan_dist(start, goal), 0, start)]`
2. TANT QUE `to_visit_heap` n'est pas vide
	21. sortir de  `to_visit_heap` la case `Case_n` prioritaire
		+ SI `Case_n` est l'arrivée, FIN de la boucle
		+ SI `Case_n` est déjà dans `intermediate_costs` avec un coût inférieur, ne rien faire et reprendre la boucle avec la case prioritaire suivante
	22. pour chacune de ses 4 cases voisines
		+ SI `Voisin_n`  est accessible (pas de mur) et n'est pas déjà dans  `intermediate_costs` avec un coût `g()` inférieur
			+ on ajoute `Voisin_n` à `intermediate_costs`, `previous_cells` et  `to_visit_heap` 
3. si `Case_end` n'est pas dans `previous_cells` à la sortie de la boucle
	+ retourne une liste liste
4. Parcourt `previous_cells` depuis  `Case_end`  jusque  `Case_start grâce aux antéc´dents
5. Retourne le résultat inversé