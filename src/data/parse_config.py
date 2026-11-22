"""Validate and load the Pac-Man game configuration."""

from pathlib import Path
import commentjson
import logging
from typing import Annotated, Any
from pydantic import (
    BaseModel,
    model_validator,
    Field,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)
from ..utils.paths import resource_path

FILENAME_REGEX = r"^([a-zA-Z0-9_\-]+/)*[a-zA-Z0-9_\-]+\.json$"
MIN_LEVELS = 10
DEFAULT_SIZE = 15
DEFAULT_CONFIG: dict[str, Any] = {
    # Relative path from the ROOT of the project
    "highscore_filename": "src/data/default_scores.json",
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
    "points_per_pacgum": 25,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 300
}


def levels_fallback(
    levels_raw: Any,
    do_pydantic: ValidatorFunctionWrapHandler,
    infos: ValidationInfo,
) -> Any:
    """Validate levels
    and replace invalid or incomplete values with defaults.

    ARGS:
    levels_raw: raw value read from the JSON
    do_pydantic: function that starts the standard Pydantic validation
    infos: information regarding validation (field name, etc.)
    """
    log_msg = []

    try:
        levels = do_pydantic(levels_raw)
    except ValidationError as error:
        details = ", ".join([err["msg"] for err in error.errors()])
        log_msg.append(f"\n\tDefault levels used for {infos.field_name}"
                       f"\n\tbecause values were invalid: {details}")
        levels = do_pydantic(DEFAULT_CONFIG["level"])

    if len(levels) < MIN_LEVELS:
        log_msg.append(f"\n\tOnly {len(levels)} levels found, "
                       f"padded to {MIN_LEVELS} with defaults")
        levels += [LvlConfig(**d)
                   for d in DEFAULT_CONFIG["level"][len(levels):MIN_LEVELS]]

    corrected_levels = []
    for expected_id, lvl in enumerate(levels, start=1):
        if lvl.id == expected_id:
            corrected_levels.append(lvl)
        else:
            log_msg.append(f"\n\tLevel id {lvl.id} replaced by {expected_id}")
            corrected_lvl = lvl.model_copy(update={'id': expected_id})
            corrected_levels.append(corrected_lvl)
    levels = corrected_levels

    if log_msg:
        logging.warning("".join(log_msg))

    return levels


def fallback(default_value: Any) -> WrapValidator:
    """Return a validator that replaces invalid values with a default."""

    def return_default(
        value_raw: Any,
        do_pydantic: ValidatorFunctionWrapHandler,
        infos: ValidationInfo,
    ) -> Any:
        """Validate a value and log when the configured default is used.
        (could be renamed `validate_or_default()` for greater precision)

    ARGS:
    levels_raw: raw value read from the JSON
    do_pydantic: function that starts the standard Pydantic validation
    infos: information regarding validation (field name, etc.)
    """
        try:
            return do_pydantic(value_raw)
        except ValidationError as error:
            details = ", ".join(err["msg"] for err in error.errors())
            log = (f"\n\tDefault value '{default_value}' used "
                   f"for {infos.field_name}\n\tbecause "
                   f"'{value_raw}' was invalid: {details}")
            logging.warning(log)
            return default_value

    return WrapValidator(return_default)


class ConfigModel(BaseModel):
    """Provide shared validation behavior for configuration models."""

    @model_validator(mode="before")
    @classmethod
    def warn_key_problems(cls, data: Any) -> Any:
        """Log unknown or missing configuration keys before validation."""
        if isinstance(data, dict):
            expected = set(cls.model_fields)
            unknown = sorted(set(data) - expected)
            missing = sorted(expected - set(data))
            if unknown:
                logging.info(f"\n\t{cls.__name__}: unknown keys "
                             f"ignored: {', '.join(unknown)}")
            if missing:
                logging.info(f"\n\t{cls.__name__}: missing keys, "
                             f"defaults used: {', '.join(missing)}")
        return data


class LvlConfig(ConfigModel):
    """Store and validate the dimensions and identifier of one level."""

    id: Annotated[int, Field(ge=1), fallback(1)] = 1
    width: Annotated[int, Field(ge=3, le=15), fallback(DEFAULT_SIZE)
                     ] = DEFAULT_SIZE
    height: Annotated[int, Field(ge=3, le=15), fallback(DEFAULT_SIZE)
                      ] = DEFAULT_SIZE


class GameConfig(ConfigModel):
    """Store and validate the complete Pac-Man game configuration."""

    highscore_filename: Annotated[
        str, Field(pattern=FILENAME_REGEX),
        fallback(DEFAULT_CONFIG["highscore_filename"]),
    ] = DEFAULT_CONFIG["highscore_filename"]

    level: Annotated[
        list[LvlConfig],
        WrapValidator(levels_fallback),
    ] = Field(default_factory=lambda: [
            LvlConfig(**d) for d in DEFAULT_CONFIG["level"]])

    lives: Annotated[
        int, Field(gt=0), fallback(DEFAULT_CONFIG["lives"]),
    ] = DEFAULT_CONFIG["lives"]
    points_per_pacgum: Annotated[
        int, Field(gt=0), fallback(DEFAULT_CONFIG["points_per_pacgum"]),
    ] = DEFAULT_CONFIG["points_per_pacgum"]
    points_per_super_pacgum: Annotated[
        int, Field(gt=0), fallback(DEFAULT_CONFIG["points_per_super_pacgum"]),
    ] = DEFAULT_CONFIG["points_per_super_pacgum"]
    points_per_ghost: Annotated[
        int, Field(gt=0), fallback(DEFAULT_CONFIG["points_per_ghost"]),
    ] = DEFAULT_CONFIG["points_per_ghost"]
    seed: Annotated[
        int, fallback(DEFAULT_CONFIG["seed"]),
    ] = DEFAULT_CONFIG["seed"]
    level_max_time: Annotated[
        int, Field(gt=0), fallback(DEFAULT_CONFIG["level_max_time"]),
    ] = DEFAULT_CONFIG["level_max_time"]


def ensure_highscore_dir(config: GameConfig) -> GameConfig:
    """Resolve the highscore path from the project root and create its dir.

    Fall back to the default path if the directory cannot be created.
    """
    default_name = DEFAULT_CONFIG["highscore_filename"]
    path = Path(resource_path(config.highscore_filename))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        logging.warning(f"\n\tCannot create the directory for "
                        f"'{path}':\n\t{err}\n\t"
                        f"Default value '{default_name}' used "
                        f"for highscore_filename")
        path = Path(resource_path(default_name))
    return config.model_copy(update={"highscore_filename": str(path)})


def get_valid_config(filename: str) -> GameConfig:
    """Load, validate, and return a game configuration from a JSON file."""
    config_path = Path(filename)
    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            config_raw = commentjson.load(config_file)
            if not (isinstance(config_raw, dict)):
                raise ValueError("Config file is not a dict:")
    except FileNotFoundError:
        logging.warning(f"Config file {config_path} is missing:"
                        "\ta default config will be loaded")
        config_raw = DEFAULT_CONFIG
    except PermissionError:
        logging.warning(f"You have no permission to read {config_path}:"
                        "\ta default config will be loaded")
        config_raw = DEFAULT_CONFIG
    except OSError as err:
        logging.warning(f"Error encountered with {config_path}: {err}"
                        "\ta default config will be loaded")
        config_raw = DEFAULT_CONFIG
    except commentjson.JSONLibraryException:
        logging.warning("Config file has invalid syntax:"
                        "\ta default config will be loaded")
        # as e To display details (still a mess when cut off before traceback)
        # err = str(e).split("Traceback")[0].strip()
        # logging.warning(err)
        config_raw = DEFAULT_CONFIG
    except ValueError as err:
        logging.warning(f"{err}\n\ta default config will be loaded")
        config_raw = DEFAULT_CONFIG

    try:
        config_validated = GameConfig.model_validate(config_raw)
    except ValidationError as err:
        logging.warning(f"Config validation error:\n\t{err}")
        config_validated = GameConfig(**DEFAULT_CONFIG)

    return ensure_highscore_dir(config_validated)
