
# Constantes et logger
```python
# chemin par défaut du fichier de scores (! relatif au dossier depuis lequel le programme est lancé... ToDo: à gérer avec PyInstaller )
PATH_SCORES = "src/data/highscores.json"
# longueur max pseudo, mesurée APRÈS `strip()`
MAX_USERNAME_LENGTH = 10
# nb max scores conservés dans le fichier, limite par défaut de `get_top_scores()`
MAX_STORED_SCORES = 10
# pour les `logger.warning()` affichés sur `stderr`
logger = logging.getLogger(__name__)
```


## Validation
#### `username_errors()`
```python
def username_errors(raw_user: object) -> str | None:
```
+ vérifie le pseudo :
	- texte,
	- non vide, pas que des espaces,
	- maxi 10 caractères,
	- uniquement des lettres, chiffres et espaces.
+ retourne soit un messageries: list[HighScore], limit: int) -> list[HighScore]:
```
+ trie les scores du plus grand au plus petit ;
+ garde les `limit` premiers (à égalité, l'ancien score reste devant) ;
+ retourne une NOUVELLE liste (la liste reçue n'est pas modifiée).

#### dataclass `LoadResult`
classe de données, pour stocker le résultat d'une tentative de lecture de `highscores.json`
```python
@dataclass(frozen=True) dès la 1ère erreur trouvée, soit `None` si tout est ok.
~~+ ToDo ==`/!\`== lettres / chiffres au sens `isalnum()`... donc lettres accentuées et non latines : **pas glop pour Nominoé**~~

#### `score_errors()` 
```python
def score_errors(raw_score: object) -> str | None:
```
+ vérifie que le score est un entier >= 0 (refuse les bool, float et string)
+ retourne soit un message d'erreur, soit `None` si tout est ok.

#### dataclass `HighScore`
petite classe de données immuable (pseudo + score) 
```python
@dataclass(frozen=True)
class HighScore:
```
+ `frozen=True` : attributs non modifiables, on est sûr que l'objet sera ensuite TOUJOURS valide.
+ se valide elle-même à la création via `__post_init__()` qui s'ajoute au `__init__` automatique pour appliquer des règles supplémentaires.
+ lève une `ValueError` si username ou score contient une erreur.

==`/!\`== `HighScore` ne nettoie PAS le pseudo : `HighScore(" Newbie ", 1)` est accepté et garde ses espaces.
=> c'est l'appelant qui DOIT faire `strip()` AVANT (cf `add_score()` et `_json_item_to_highscore()`).


## Stockage
#### `sorted_limit_best()`
utilitaire pour `add_score()` et `get_top_scores()`
```python
def sorted_limit_best(entries: list[HighScore], limit: int) -> list[HighScore]:
```
+ trie les scores du plus grand au plus petit ;
+ garde les `limit` premiers (à égalité, l'ancien score reste devant) ;
+ retourne une NOUVELLE liste (la liste reçue n'est pas modifiée).

#### dataclass `LoadResult`
classe de données, pour stocker le résultat d'une tentative de lecture de `highscores.json`
```python
@dataclass(frozen=True)
class LoadResult:
    entries: list["HighScore"]
    corrupted: bool
```
- liste des scores valides
- flag `True` / `False` indiquant un souci avec le fichier

==`ToDo`== supprimer `frozen=True` car `add_score()` fait un `.append()` sur `entries`
(`frozen` empêche de réassigner `entries` ou `corrupted`, MAIS pas de modifier la liste elle-même... :P).


#### classe `HighScoreStorage`
Gère le stockage, LECTURE / ÉCRITURE, du fichier JSON

```python
# initialise le chemin d'accès au fichier de sauvegarde
def __init__(self, file_path: str | Path = PATH_SCORES) -> None:
```
- accepte une string ou un objet Path, par défaut `PATH_SCORES` = `"src/data/highscores.json"` (! ==`ToDo`== chemin relatif au dossier de lancement).
- transforme l'argument reçu en un objet `Path` robuste... pour avoir accès à toutes les chouettes méthodes de `pathlib`, par ex :
    - .exists() pour vérifier si le fichier existe
    - .read_text() pour lire le JSON les doigts dans le nez
    - en bonus, assure la compatibilité avec les chemins Windows (`\`) et Linux/Mac (`/`).
- ne crée ni fichier ni dossier

  
```python
# convertit 1 élt brut extrait de `highscores.json`, en un objet `HighScore` valide et nettoyé
def _json_item_to_highscore(self, item: object) -> HighScore | None:
```
  - transforme un dictionnaire JSON en `HighScore`,
  - retourne l'objet validé
  - ou bien `None` si :
	- l'objet reçu n'est pas un dictionnaire
	- si la clé `username` n'existe pas
	- si la valeur de `username` n'est pas valide
	- si la clé `score` n'existe pas
	- si la valeur de `score` n'est pas valide
	(d'éventuelles clés supplémentaires sont ignorées)


```python
# gère lecture+décodage+validation des scores stockés dans le fichier JSON
def _load_raw(self) -> LoadResult:
```
................................ WORK IN PROGRESS ......................................
  - lit le fichier,
	  - le décode,
	  - valide chaque entrée,
	  - signale si le fichier est corrompu.
  
  - `load_scores()`
	  - retourne seulement la liste des scores valides.
  
  - `_copy_corrupted_file()`
	  - fait une copie de sauvegarde d'un fichier corrompu avant de l'écraser.
  
  - `_write_all()`, pour ne jamais laisser un fichier à moitié écrit
	  - écrit la liste complète dans un fichier temporaire,
	  - puis le renomme.
  
  - `add_score()`
	  - valide un score,
	  - puis l'ajoute,
	  - et ne garde que les meilleurs.
  
  - `get_top_scores()`
	  - retourne les meilleurs scores triés.


# @dataclass(frozen=True)

`frozen=True` garantit que, n'importe où dans le code, chaque objet a passé la validation.  

=> utilisé pour `HighScore`


#### Contexte

A la création d'un objet `Highscore`,  `__post_init__()` refuse les données invalides :
```python
HighScore("Alice", -50)   # ValueError : le score ne peut pas être négatif :P
```


#### Un `HighScore` qui existe est forcément valide,
inutile de revérifier à chaque endroit du code :

- Sans `frozen=True`, on pourrait créer un score valide, puis le remplacer après coup, sans aucune vérification :
```python
high_score = HighScore("Alice", 100)   # valide
high_score.score = -50                 # invalide mais accepté sans vérif !
high_score.username = "@@@???"         # invalide mais accepté sans vérif !
```
=> le code qui reçoit ensuite `high_score` croit avoir un score valide, alors que ce n'est plus vrai !

- Avec `frozen=True`, on ne peut pas "casser" un score valide après coup, sans aucune vérif :
```python
high_score = HighScore("Alice", 100)   # valide
high_score.score = -50                 # lève illico une FrozenInstanceError car invalide
high_score.username = "@@@???"         # lève illico une FrozenInstanceError car invalide
```


#### Pas de modif accidentelle
quand on partage les objets :

- `avantage` : avec des objets figés par `frozen=True`, on peut trimbaler les objets partout sans risque d'une modif par effet de bord.
par ex les `highscore`` circulent entre plusieurs listes :
```python
all_scores = storage.load_scores()
top3 = sorted_limit_best(all_scores, 3)   # "top3" contient les MÊMES objets que "all_scores"
```
=> sans `frozen=True`, du code modifiant un score dans `top3`... modifierait aussi celui de `all_scores` (potentiel bug difficile à identifier)

- `contrainte` : on ne peut pas nettoyer un champ après coup...
```python
# obligation de `strip()` AVANT de créer l'objet :
HighScore(username=username.strip(), ...)
# car le `strip()` échouerait dans `__post_init__()` :
self.username = self.username.strip()
```


#### Objets **hashables** :
être hashable permet de servir de clé dans un `dict` ou de membre dans un `set` :D
- Par défaut, une @dataclass classique n'est pas hashable puisque ses données peuvent changer.
- Avec `frozen=True`, Python génère automatiquement une méthode __hash__ basée sur les champs de la classe.
```python
@dataclass(frozen=True)
class Point:
    x: int
    y: int

# Valide, car l'objet est frozen et donc hashable
positions = {Point(0, 0): "Départ", Point(10, 5): "Arrivée"} 
```


#### Supprimer `frozen=True` dans `LoadResult`... ou pas :
- ok exprime bien l'intention : résultat de la lecture, à un instant T et qu'on n'a pas de raison de modifier ;
- ko interdit de réassigner `result.entries` MAIS pas de modifier la liste qu'elle contient...
  cf `add_score()` qui modifie la liste (à l'intérieur de l'objet censé être figé), avec `entries = result.entries` puis `entries.append(...)`.
- MAIS, le supprimer déclenche une avalanche de ronchonades mypy