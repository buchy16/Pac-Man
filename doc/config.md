# Error handling

### Contraintes validées par  `Pydantic`

+ `highscore_filename` : chaîne respectant la regex `^[a-zA-Z0-9_\-]+\.json$`
+ `lives` : entier > 0
+ `points_per_pacgum` : entier > 0
+ `points_per_super_pacgum` : entier > 0
+ `points_per_ghost` : entier > 0
+ `seed` : entier
+ `level_max_time` : entier > 0
+ `level` : liste de 10 éléments minimum ;
    et pour chaque élément :
    + `id` : entier à partir de 1, sans doublon et consécutifs
    + `width` : 3 <= entier <= 15
    + `height` : 3 <= entier <= 15
      (l'affichage dans une fenêtre de 1280×720 pixels, avec des tuiles de 48×48 pixels, justifie la limite de 15 cases)
### Comportement en cas de valeur invalide

+ `ERROR`
	+ le nombre d'arguments reçus est différent de 1
	  => le programme s'arrête avec le code de sortie `1`.

+ `WARNING`
	+ le fichier est manquant, ou illisible (problème d'accès ou erreur de lecture)
	  => la configuration par défaut est utilisée.
	+ la validation globale échoue, le JSON est syntaxiquement invalide
	  => la configuration par défaut est utilisée.
	+ une valeur est invalide ou manquante
	  => la valeur par défaut est utilisée.

+ `INFO`
	+ une clé est inconnue
	  => elle est ignorée.
	+ une clé est manquante
	  => elle est ajoutée avec sa valeur par défaut.

# Exemple de journalisation et correction

### configuration erronée :
```json
{
    "highscore_filename": "high, scores.json",
    "bonus": 99,
    "points_per_pacgum": "ten",
    "seed": 42,
    "level_max_time": 0,
    "level": [
        {"id": 99, "width": 12, "height": 12},
        {"id": 2, "width": -13, "height": 13},
        {"id": 10, "width": 14}
    ]
}
```

### Journaux :
```
INFO: 
	GameConfig: unknown keys ignored: bonus
INFO: 
	GameConfig: missing keys, defaults used: lives, points_per_ghost, points_per_super_pacgum
WARNING: 
	Default value 'highscores.json' used for highscore_filename
	because 'high, scores.json' was invalid: String should match pattern '^[a-zA-Z0-9_\-]+\.json$'
WARNING: 
	Default value '15' used for width
	because '-13' was invalid: Input should be greater than or equal to 3
INFO: 
	LvlConfig: missing keys, defaults used: height
WARNING: 
	Only 3 levels found, padded to 10 with defaults
	Level id 99 replaced by 1
	Level id 10 replaced by 3
WARNING: 
	Default value '10' used for points_per_pacgum
	because 'ten' was invalid: Input should be a valid integer, unable to parse string as an integer
WARNING: 
	Default value '90' used for level_max_time
	because '0' was invalid: Input should be greater than 0
```

### configuration validée :
```python
highscore_filename='highscores.json'
lives=3
points_per_pacgum=10
points_per_super_pacgum=50
points_per_ghost=200
seed=42
level_max_time=90
level=[
    LvlConfig(id=1, width=12, height=12),
    LvlConfig(id=2, width=15, height=13),
    LvlConfig(id=3, width=14, height=15),
    LvlConfig(id=4, width=15, height=15),
    LvlConfig(id=5, width=15, height=15),
    LvlConfig(id=6, width=15, height=15),
    LvlConfig(id=7, width=15, height=15),
    LvlConfig(id=8, width=15, height=15),
    LvlConfig(id=9, width=15, height=15),
    LvlConfig(id=10, width=15, height=15)
]
```