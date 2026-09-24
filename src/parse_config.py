from pathlib import Path

import commentjson
from pydantic import (BaseModel, ConfigDict, Field, ValidationError,
                      field_validator, model_validator)

from .utils import print_green, print_red


# sous-structure pour les niveaux
class LevelConfig(BaseModel):
    id: int = Field(default=1, ge=1, le=10)
    width: int = Field(default=15, ge=14, le=30)
    height: int = Field(default=15, ge=10, le=16)


# structure principale
class GameConfig(BaseModel):
    # extra="forbid": toute clé du JSON qui ne correspond à aucun champ déclaré
    # fait échouer la validation, au lieu d'être ignorée silencieusement
    model_config = ConfigDict(extra="forbid")

    highscore_filename: str
    level: list[LevelConfig]  # liste d'objets `LevelConfig`

    # Validations basiques
    lives: int = Field(default=3, gt=0)
    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90, gt=0)

    @field_validator('highscore_filename')
    @classmethod
    def check_json_ext(cls, file_name: str) -> str:
        if not file_name.lower().endswith('.json'):
            raise ValueError("The file must end with '.json'")
        return file_name

    # règles métier (validations croisées), 'after' la vérif des types de base
    @model_validator(mode='after')
    def verifier_coherence_points(self):
        # la super pacgum doit rapporter plus que l'ordinaire
        if self.points_per_pacgum >= self.points_per_super_pacgum:
            raise ValueError(
                "What a scam! points_per_super_pacgum "
                f"({self.points_per_super_pacgum}) "
                "should be greater than points_per_pacgum "
                f"({self.points_per_pacgum})."
            )
        # miam-miam ghost doit rapporter plus que la super pacgum
        if self.points_per_super_pacgum >= self.points_per_ghost:
            raise ValueError(
                f"What a scam! points_per_ghost ({self.points_per_ghost}) "
                "should be greater than points_per_super_pacgum "
                f"({self.points_per_super_pacgum})."
            )
        # tout est OK, on peut renvoyer l'objet
        return self

    @model_validator(mode='after')
    def verifier_niveaux(self):
        # les id des niveaux doivent être uniques
        ids = [lvl.id for lvl in self.level]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate level ids found: {ids}")
        # mandatory : fournir 10 niveaux minimum
        if len(self.level) < 10:
            raise ValueError("The game requires at least ten levels.")
        return self


def parse_validate_config(chemin_fichier: str | Path) -> GameConfig:
    """Parse et valide le fichier de configuration du jeu.

    Laisse remonter les exceptions pertinentes :
    l'appelant décide comment les présenter (console, log, interface graph...)

    Args:
        chemin_fichier: Chemin vers le fichier de configuration
            (JSON pouvant inclure commentaires ``#`` et ``//``)
            ajouté type Path car la fixture tmp_path pytest donne un objet Path

    Returns:
        GameConfig: la configuration validée

    Raises:
        FileNotFoundError: qd le fichier n'existe pas.
        commentjson.JSONLibraryException: contenu JSON invalide
        pydantic.ValidationError: règles de validation non respectées
    """
    chemin = Path(chemin_fichier)

    with chemin.open("r", encoding="utf-8") as a_file:
        config_raw = commentjson.load(a_file)

    return GameConfig(**config_raw)


def parsing(file_path: str) -> None:
    """Point d'entrée appelé depuis __main__.py, pour tester le parsing."""
    try:
        config = parse_validate_config(file_path)
    except FileNotFoundError as err:
        print_red(f"Config file is missing : {err}")
        return
    except commentjson.JSONLibraryException as e:
        # BOF, reste moche même en coupant avant le traceback
        err = str(e).split("Traceback")[0].strip()
        print_red(f"Config file has invalid syntax :\n{err}")
        return
    except ValidationError as err:
        print_red(f"Config validation error : {err}")
        return

    print_green("Config is valid and ready to use!")
