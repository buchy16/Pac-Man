# Error handling

### Contraintes validées par  `Pydantic`

+ `highscore_filename` : chaîne respectant la regex `r"^([a-zA-Z0-9_\-]+/)*[a-zA-Z0-9_\-]+\.json$"`
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

# `parse_config.py`

```python
# objet Path = chemin de fichier, plus pratique qu'un str
from pathlib import Path
import commentjson
import logging
# Annotated: pour attacher des règles de validation à un type
from typing import Annotated, Any
# boite à outils Pydantic :
from pydantic import (
    BaseModel,                    # classe de base de tous les modèles
    model_validator,              # décorateur pour valider un modèle entier
    Field,                        # règles sur un champ (ge, le, gt, pattern)
    ValidationError,              # erreur levée quand une valeur est invalide
    ValidationInfo,               # infos sur la validation en cours (nom du champ, par ex)
    ValidatorFunctionWrapHandler, # fonction qui lance la validation normale
    WrapValidator,                # validateur qui "enveloppe" la validation
)
# resource_path ajoutera la racine du projet devant les chemins relatifs
from ..utils.paths import resource_path


# regex pour accepter un chemin incluant des dossiers
#   ^                      début de la chaîne
#   (                      début d'un groupe : "un dossier"
#     [a-zA-Z0-9_\-]+      un nom : lettres chiffres _ -
#     /                    suivi d'un slash
#   )*                     ce groupe peut être répété n fois
#   [a-zA-Z0-9_\-]+        nom du fichier (non vide)
#   \.json                 un vrai point, puis "json"
#   $                      fin de la chaîne
# valides : "scores.json", "src/data/scores.json"
# non valides : "/etc/scores.json", "src//scores.json", "../scores.json"
FILENAME_REGEX = r"^([a-zA-Z0-9_\-]+/)*[a-zA-Z0-9_\-]+\.json$"
MIN_LEVELS = 10
DEFAULT_SIZE = 15
DEFAULT_CONFIG: dict[str, Any] = {
    # Chemin relatif à la RACINE du projet
    "highscore_filename": "src/data/defaultscores.json",
    "level": [
        {"id": 1, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 2, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 3, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 4, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 5, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 6, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 7, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 8, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 9, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE},
        {"id": 10, "width": DEFAULT_SIZE, "height": DEFAULT_SIZE}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}


# ============================================================================
# FONCTIONS DE REPLI (valeurs par défaut)
# ============================================================================


# Validateur "wrap" : pydantic l'appelle à la place de sa validation normale,
# avec 3 paramètres
def levels_fallback(
    levels_raw: Any,                        # valeur brute lue dans le JSON
    do_pydantic: ValidatorFunctionWrapHandler,  # lance la validation normale
    infos: ValidationInfo,                  # infos (nom du champ, etc.)
) -> Any:
    """
    valide la liste des niveaux,
    la complète avec des niveaux par défaut si elle est trop courte,
    et renumérote les id de 1 à n.
    """
    # pour stocker les élts du log à afficher
    log_msg = []

    # tente la validation normale
    try:
        # transformer la liste de dictionnaires en liste d'objets LvlConfig
        levels = do_pydantic(levels_raw)

    except ValidationError as error:
        # error.errors() = liste des erreurs, dont on extrait les valeurs de "msg"
        details = ", ".join([err["msg"] for err in error.errors()])
        log_msg.append(f"\n\tDefault levels used for {infos.field_name}"
                       f"\n\tbecause values were invalid: {details}")
        # et on refourgue la liste de niveaux par défaut
        levels = do_pydantic(DEFAULT_CONFIG["level"])

    # si il manque des niveaux... on ajoute les niveaux par défaut manquants.
    if len(levels) < MIN_LEVELS:
        log_msg.append(f"\n\tOnly {len(levels)} levels found, "
                       f"padded to {MIN_LEVELS} with defaults")

        # [len(levels):MIN_LEVELS] pour choper les numéros de level manquants
        # "**d" transforme le dict en arguments nommés (id=..., width=..., height=...).
        # pour instancier un nouvel objet LvlConfig
        # et on ajoute ces nvx niveaux à ceux existants
        levels += [LvlConfig(**d)
                   for d in DEFAULT_CONFIG["level"][len(levels):MIN_LEVELS]]

    # les levels devront aussi contenir des id consécutifs de 1 à n
    corrected_levels = []

    # l'id du n-ième niveau doit valoir n
    for expected_id, lvl in enumerate(levels, start=1):
        # Si l'id est ok, on garde le niveau tel quel
        if lvl.id == expected_id:
            corrected_levels.append(lvl)

        # sinon, ne pas modifier l'original : créer une copie du niveau avec l'id correct
        else:
            log_msg.append(f"\n\tLevel id {lvl.id} replaced by {expected_id}")
            corrected_lvl = lvl.model_copy(update={'id': expected_id})
            corrected_levels.append(corrected_lvl)

    levels = corrected_levels

    if log_msg:
        # et hop, tous les logs en même temps dans la console :D
        logging.warning("".join(log_msg))

    # et hop, v'là le champ "level" valide :D
    return levels


# Fabrique et renvoie un validateur qui remplace une valeur invalide par default_value.
# cf "closure" de la piscine Python :
# fonction qui renvoie une fonction, default_value est mémorisée à l'intérieur :D
def fallback(default_value: Any) -> WrapValidator:
    """Return a validator that replaces invalid values with a default."""

    # return_default() est appelée par pydantic pour chaque valeur du champ
    # à renommer `validate_or_default()` pour être plus précis
    def return_default(
        value_raw: Any,                             # valeur brute à valider
        do_pydantic: ValidatorFunctionWrapHandler,  # validation normale
        infos: ValidationInfo,                      # infos (nom du champ...)
    ) -> Any:
        """Tente la validation,
        log et renvoie le défaut en cas d'échec."""

        # tente la validation normale
        try:
            return do_pydantic(value_raw)

        except ValidationError as error:
            # assemble les erreurs pour le log
            details = ", ".join(err["msg"] for err in error.errors())
            log = (f"\n\tDefault value '{default_value}' used "
                   f"for {infos.field_name}\n\tbecause "
                   f"'{value_raw}' was invalid: {details}")
            logging.warning(log)
            # et retourne la valeur par défaut
            return default_value

    # emballe return_default dans un WrapValidator que pydantic comprend.
    return WrapValidator(return_default)


def ensure_highscore_dir(config: GameConfig) -> GameConfig:
    return config.model_copy(update={"highscore_filename": str(path)})
    """
    retourne le chemin complet du fichier de scores à partir de la racine du projet
    si besoin crée son dossier, revient au chemin par défaut si la création échoue
    """
    default_name = DEFAULT_CONFIG["highscore_filename"]
    path = Path(resource_path(config.highscore_filename))

    # tente de créer le dossier
    try:
        # parents=True pour créer aussi les dossiers intermédiaires manquants
        # exist_ok=True pour pas râler si le dossier existe déjà
        path.parent.mkdir(parents=True, exist_ok=True)

    # droits refusés, nom déjà pris par un fichier...
    except OSError as err:
        logging.warning(f"\n\tCannot create the directory for "
                        f"'{path}':\n\t{err}\n\t"
                        f"Default value '{default_name}' used "
                        f"for highscore_filename")
        # on repart du chemin par défaut
        path = Path(resource_path(default_name))

    # renvoie une COPIE de la config
    # avec un chemin VALIDE et complet, en str comme exigé par le champ
    return config.model_copy(update={"highscore_filename": str(path)})

```