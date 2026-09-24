from typing import Any

import pytest
from pydantic import ValidationError

from src.parse_config import GameConfig, LevelConfig

# ===========================================================================
#                                          DICTIONNAIRES VALIDES de référence
# ===========================================================================

@pytest.fixture
def a_valid_level() -> dict[str, Any]:
    """Provide a valid level configuration dictionary.

    Returns:
        dict[str, Any]: a dict containing all fields accepted by `LevelConfig`
        (`id`, `width`, `height`) with values that pass validation.
    """
    return {"id": 1, "width": 15, "height": 15}


@pytest.fixture
def a_valid_config(a_valid_level: dict[str, Any]) -> dict[str, Any]:
    """Provide a valid game configuration dictionary.

    Args:
        a_valid_level (dict[str, Any]): `a_valid_level` fixture,
          reused as the single entry of the `level` list.

    Returns:
        dict[str, Any]: a dict containing all required `GameConfig` fields
          (`highscore_filename`, `level`, ...)
          => tests mutate a copy of this fixture with specific invalid values.
    """
    return {
        "highscore_filename": "highscores.json",
        "level": [a_valid_level],
        "lives": 3,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
        "level_max_time": 90,
    }


# ===========================================================================
#                                                                LEVEL CONFIG
# ===========================================================================

# ---------------------------------------------------------------------------
#                                                        level default values
# ---------------------------------------------------------------------------
def test_level_defaults() -> None:
    """Verify that `levelConfig` uses the documentation's default values. """
    level = LevelConfig()

    assert level.id == 1
    assert level.width == 15
    assert level.height == 15

# ---------------------------------------------------------------------------
#                                                  bad values in level fields
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("a_field, invalid_value", [
    ("id", 0),        # off the map: < 1
    ("id", 11),       # off the map: > 10
    ("width", 13),    # off the map: < 14
    ("width", 31),    # off the map: > 30
    ("height", 9),    # off the map: < 10
    ("height", 17),   # off the map: > 16
])
def test_level_field_out_of_bounds(a_valid_level: dict[str, Any],
                                   a_field: str, invalid_value: int) -> None:
    """Verify that out-of-range LevelConfig values raise a `ValidationError`.

    Args:
        a_valid_level (dict[str, Any]): the `a_valid_level` fixture.
        a_field (str): The field under test (`"id"`, `"width"` or `"height"`).
        invalid_value (int): The out-of-bounds value to assign to`a_field`.
    """
    a_valid_level[a_field] = invalid_value

    with pytest.raises(ValidationError):
        LevelConfig(**a_valid_level)


# ===========================================================================
#                                                     MISSING or EXTRA FIELDS
# ===========================================================================

# ---------------------------------------------------------------------------
#                                                              missing fields
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("missing_field", ["highscore_filename", "level"])
def test_missing_required_field(a_valid_config: dict[str, Any],
                                missing_field: str) -> None:
    """Verify that omitting a required GameConfig field raises an error.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
        missing_field (str): field to remove from config before validation.
    """
    del a_valid_config[missing_field]

    with pytest.raises(ValidationError):
        GameConfig(**a_valid_config)

# ---------------------------------------------------------------------------
#                                                                extra fields
# ---------------------------------------------------------------------------
def test_extra_field_forbidden(a_valid_config: dict[str, Any]) -> None:
    """Verify that an unknown extra field raises a `ValidationError`.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
    """
    a_valid_config["not_expected_field"] = "unexpected bonus"

    with pytest.raises(ValidationError):
        GameConfig(**a_valid_config)


# ===========================================================================
#                                                              HIGHSCORE FILE
# ===========================================================================
@pytest.mark.parametrize("invalid_name", ["highscores.txt", "highscores",
                                          "highscores.json.bak"])
def test_highscore_file_ext_not_json(a_valid_config: dict[str, Any],
                                     invalid_name: str) -> None:
    """Verify that no `.json` extension `highscore_filename` fails validation.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
        invalid_name (str): a filename that does not end with `.json`.
    """
    a_valid_config["highscore_filename"] = invalid_name

    with pytest.raises(ValidationError):
        GameConfig(**a_valid_config)


# ===========================================================================
#                                                            LEVEL LIST RULES
# ===========================================================================

# ---------------------------------------------------------------------------
#                                                            empty level list
# ---------------------------------------------------------------------------
def test_empty_level_list(a_valid_config: dict[str, Any]) -> None:
    """Verify that an empty `level` list raises a `ValidationError`.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
    """
    a_valid_config["level"] = []

    with pytest.raises(ValidationError):
        GameConfig(**a_valid_config)

# ---------------------------------------------------------------------------
#                                                          at least 10 levels
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("nb_levels", [0, 10])
def test_at_least_ten_levels(a_valid_config: dict[str, Any], nb_levels: int) -> None:
    """Verify that less than 10 levels raises a `ValidationError`.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
    """
    a_valid_config["level"] = [
        {"id": i, "width": 15, "height": 15} for i in range(1, nb_levels)
    ]

    with pytest.raises(ValidationError, match="The game requires at least ten levels"):
        GameConfig(**a_valid_config)

# ---------------------------------------------------------------------------
#                                                         duplicated level id
# ---------------------------------------------------------------------------
def test_duplicated_level_id(a_valid_config: dict[str, Any],
                             a_valid_level: dict[str, Any]) -> None:
    """Verify that duplicate level ids raise a ``ValidationError``.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
        a_valid_level (dict[str, Any]): the `a_valid_level` fixture.
    """
    duplicate = a_valid_level.copy()
    a_valid_config["level"] = [a_valid_level, duplicate]

    with pytest.raises(ValidationError, match="Duplicate level ids"):
        GameConfig(**a_valid_config)


# ---------------------------------------------------------------------------
#                                               distincts levels from 1 to 10
# ---------------------------------------------------------------------------
def test_multiple_distinct_levels_ok(a_valid_config: dict[str, Any]) -> None:
    """Verify that many levels with distinct id validate successfully.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
    """
    a_valid_config["level"] = [
        {"id": i, "width": 15, "height": 15} for i in range(1, 11)
    ]

    config = GameConfig(**a_valid_config)

    assert len(config.level) == 10


# ===========================================================================
#                                                              INVALID VALUES
# ===========================================================================

# ---------------------------------------------------------------------------
#                                                      invalid numeric values
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("a_field, invalid_value", [
    ("lives", 0),                      # must be > 0
    ("lives", -1),
    ("level_max_time", 0),             # must be > 0
    ("level_max_time", -10),
    ("points_per_pacgum", -1),         # must be >= 0
    ("points_per_super_pacgum", -1),   # must be >= 0
    ("points_per_ghost", -1),          # must be >= 0
])
def test_numeric_bounds(a_valid_config: dict[str, Any], a_field: str,
                        invalid_value: int) -> None:
    """Verify that out-of-range numeric GameConfig fields fail validation.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
        a_field (str): the numeric field under test.
        invalid_value (int): out-of-bounds value to assign to `a_field`.
    """
    a_valid_config[a_field] = invalid_value

    with pytest.raises(ValidationError):
        GameConfig(**a_valid_config)


# ===========================================================================
#                                                      POINTS COHERENCE RULES
# ===========================================================================

# ---------------------------------------------------------------------------
#                                            super_pacgum greater than pacgum
# ---------------------------------------------------------------------------
def test_super_pacgum_bigger_than_pacgum(a_valid_config: dict[str, Any]) -> None:
    """Verify that `points_per_super_pacgum < points_per_pacgum` fails.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
    """
    a_valid_config["points_per_pacgum"] = 50
    a_valid_config["points_per_super_pacgum"] = 50

    with pytest.raises(ValidationError, match="should be greater than "
                       "points_per_pacgum"):
        GameConfig(**a_valid_config)

# ---------------------------------------------------------------------------
#                                             ghost greater than super_pacgum
# ---------------------------------------------------------------------------
def test_ghost_bigger_than_super_pacgum(a_valid_config: dict[str, Any]) -> None:
    """Verify that `points_per_ghost < points_per_super_pacgum` fails.

    Args:
        a_valid_config (dict[str, Any]): the `a_valid_config` fixture.
    """
    a_valid_config["points_per_super_pacgum"] = 200
    a_valid_config["points_per_ghost"] = 200

    with pytest.raises(ValidationError, match="should be greater than "
                       "points_per_super_pacgum"):
        GameConfig(**a_valid_config)
