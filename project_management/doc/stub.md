# OBJECTIF
rendre le projet valide `mypy --strict`

==`Problème`== 
`mypy` vérifie les types en lisant les annotations (`int`, `str`, `list[int]`…).
Pour une bibliothèque externe, il a besoin de savoir quels types elle utilise.

==`BAD rustine`==
Inclure `mazegenerator` dans les `--ignore-missing-imports` du `pyproject.toml` :
```toml
[[tool.mypy.overrides]]
module = ["keysymdef.*", "mlx.*", "commentjson.*", "mazegenerator.*"]
ignore_missing_imports = true
```
=> cela dit à `mypy` de se taire et de traiter ce module comme `Any` 
**MAIS...** hériter d'une classe de type `Any`, c'est hériter d'un inconnu :
=>`mypy` ne peut plus garantir quoi que ce soit sur ses méthodes et le mode `--strict` râle

==`GOOD soluce`==
Un **stub** est un fichier `.pyi` qui décrit uniquement les types d'un module, sans aucun code :
- il liste les classes, les attributs et les signatures de fonctions ;
- il n'est **jamais exécuté** : Python l'ignore, seul mypy le lit ;
- il sert de "fiche d'identité" du module, genre "*voici ce que `MazeGenerator` contient et de quels types*".
=> `mypy` sait alors que `MazeGenerator` est une vraie classe, donc `Any` disparaît et l'erreur aussi :D


# MOD OP

## 1. Créer le dossier et le fichier

Le nom du fichier doit être **exactement** celui du module importé, par ex :
+ si `mazegenerator` est un module simple, créer `stubs/mazegenerator.pyi`
+ si `mazegenerator` est un dossier (package), créer `stubs/mazegenerator/__init__.pyi`

Donc, à la racine du projet :
```
.
├── pyproject.toml
├── src/
│   └── ...
└── stubs/
    └── mazegenerator/
        └── __init__.pyi
```

En décompressant `mazegenerator-2.1.0-py3-none-any.whl`, on peut lire son contenu pour en extraire toutes les infos requises par `mypy` :
- la déclaration de la classe
- ses attributs utilisés dans le projet (par ex. lus par `maze.py` et réécrits dans `regenerate_maze`)
- la signature du constructeur (types des paramètres et du retour, pas le corps)
  **`...`** trois points, appelé *Ellipsis*, signifie "*le corps est omis*"
- les méthodes appelées dans le projet (par ex. `regenerate_maze` appelle via `self.generate(self._seed)`)

Exemple de fichier `.pyi` :
```python
from typing import Iterator

class MazeGenerator:
    _width: int
    _height: int
    _perfect: bool
    _seed: int
    _entryx: int
    _entryy: int
    _exitx: int
    _exity: int
    _maze: list[list[int]]
    _path: list[list[int]]
    _shortest_path: str | bool

    def __init__(
        self,
        size: tuple[int, int] = ...,
        perfect: bool = ...,
        entry_cell: tuple[int, int] = ...,
        exit_cell: tuple[int, int] = ...,
        seed: int = ...,
    ) -> None: ...
    @property
    def maze(self) -> list[list[int]]: ...
    @property
    def shortest_path(self) -> str | bool: ...
    @property
    def maze_entry(self) -> tuple[int, int]: ...
    @property
    def maze_exit(self) -> tuple[int, int]: ...
    def generate(self, seed: int = ...) -> None: ...
    def _braid(self) -> None: ...
    def _create_empty_maze(self) -> None: ...
    def _add_42_to_maze(self) -> None: ...
    def _is_available(self, x: int, y: int) -> bool: ...
    def _get_neighbors(
        self, x: int, y: int
    ) -> Iterator[tuple[int, int, int, int]]: ...
    def _generate_maze(self, x: int, y: int, from_code: int) -> None: ...
    def _find_short_path(self) -> None: ...
```

## 2. renseigner `mypy`

En ajoutant dans `pyproject.toml` :
```toml
[tool.mypy]
mypy_path = "stubs"
```
on dit à `mypy` de chercher `mazegenerator` dans `stubs/` en plus des endroits habituels.
=> L'erreur `Class cannot subclass "MazeGenerator" (has type "Any")` disparaît et les deux modes (normal et `--strict`) passent :D

A noter : le chemin est relatif à l'endroit d'où est lancée la commande, donc la racine du projet, la commande `uv run mypy src ...` reste valide.

*Et ne pas oublier de virer `mazegenerator` dans `mypy.overrides`* :
```toml
[[tool.mypy.overrides]]
module = ["keysymdef.*", "mlx.*", "commentjson.*"]
ignore_missing_imports = true
```

# Pour info

+ Un stub doit **refléter le vrai module** : si on y met une signature fausse, mypy fera confiance et donnera de faux résultats...
	+ Ouvrir le code du package et comparer chaque signature : noms des paramètres, valeurs par défaut, types. Si le vrai `__init__` a des valeurs par défaut, les indiquer par `...` dans le stub : `seed: int = ...`.
	+ Un attribut ou une méthode absent du stub est une erreur pour `mypy` : il répondra `"the_module" has no attribute "xxx"`, il faut ajouter au stub tout ce que le code utilise.

+ Pour **générer un brouillon** du `.pyi` automatiquement, `mypy` fournit un outil :
   ```
   # lit le module installé et produit un `.pyi` à compléter :
   uv run stubgen -p mazegenerator -o stubs
   
   # Pour inclure les membres privés :
   uv run stubgen -p mazegenerator -o stubs --include-private
   ```
	Les types qu'il ne peut pas deviner sont écrits `Incomplete` (= `Any`), à remplacer par les vrais types.

+ **Avantages** du stub
	- plus aucun `# type: ignore` à maintenir ;
	- mypy vérifie maintenant les accès à `self._maze`, `self._width`, etc., et détecte les fautes de frappe ou les mauvais types ;
	- un bon stub reste valable si le projet grandit.

+ **vigilance** 
	une fois le stub en place, mypy contrôle réellement `maze.py` et peut faire apparaître des erreurs jusque-là masquées par `Any`.  
	Par exemple, si le stub dit `_width: int` et que le code y affecte autre chose, il le signalera..