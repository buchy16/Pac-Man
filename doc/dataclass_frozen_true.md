# @dataclass(frozen=True)

`frozen=True` garantit que, n'importe où dans le code, chaque objet a passé la validation.  

=> utilisé pour `HighScore`


### Contexte

A la création d'un objet `Highscore`,  `__post_init__()` refuse les données invalides :
```python
HighScore("Alice", -50)   # ValueError : le score ne peut pas être négatif :P
```


### Un `HighScore` qui existe est forcément valide,
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


### Pas de modif accidentelle
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


### Objets **hashables** :
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


### Ooops,
goldfish

`/!\` *copier-coller is evil...* => Supprimer `frozen=True` dans `LoadResult` :
- ok exprime bien l'intention : résultat de la lecture, à un instant T et qu'on n'a pas de raison de modifier ;
- ko interdit de réassigner `result.entries` MAIS pas de modifier la liste qu'elle contient...
  cf `add_score()` qui modifie la liste (à l'intérieur de l'objet censé être figé), avec `entries = result.entries` puis `entries.append(...)`.