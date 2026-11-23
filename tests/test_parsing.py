import pytest
import logging
from _pytest.logging import LogCaptureFixture
from pathlib import Path
from typing import Any
from src.__main__ import main
from src.data.parse_config import get_valid_config
from src.data.parse_config import DEFAULT_CONFIG, MIN_LEVELS, DEFAULT_SIZE
from src.utils.paths import resource_path


def resolved(name: str) -> str:
    """Highscore path as returned by get_valid_config() (resolved)."""
    return str(resource_path(name))


def expected_default() -> dict[str, Any]:
    """DEFAULT_CONFIG as it looks after ensure_highscore_dir()."""
    return {
        **DEFAULT_CONFIG,
        "highscore_filename": resolved(DEFAULT_CONFIG["highscore_filename"]),
    }


# ===========================================================================
#                                                                nb ARGUMENTS
# ===========================================================================

# ---------------------------------------------------------- MISSING ARGUMENT
def test_zero_argument(caplog: LogCaptureFixture) -> None:
    """Verify that the program stops if no argument is given.

    Args:
        caplog: to check the displayed message
    """
    # ne capture que les messages de niveau >= ERROR
    with caplog.at_level(logging.ERROR):
        # assertion que main doit lever une exception SystemExit
        with pytest.raises(SystemExit) as except_info:
            main(["__main__.py"])

    # assertion que le code de sortie vaut 1
    assert except_info.value.code == 1
    # assertion que la console affiche "You gave 0 argument..."
    assert "You gave 0 argument" in caplog.text


# -------------------------------------------------------- TOO MUCH ARGUMENTS
def test_multiple_arguments(caplog: LogCaptureFixture) -> None:
    """Verify that the program stops if more than 1 argument is given.

    Args:
        caplog: to check the displayed message
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit) as except_info:
            main(["__main__.py", "config.json", "too much arg"])

    assert except_info.value.code == 1
    assert "You gave 2 arguments" in caplog.text


# ===========================================================================
#                                                                 FILE ERRORS
# ===========================================================================

# -------------------------------------------------------------- FILE MISSING
def test_file_not_found(caplog: LogCaptureFixture, tmp_path: Path) -> None:
    """Verify that parsing a missing file logs the error, loads DEFAULT_CONFIG.

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
    """
    config_file = tmp_path / "missing_file.json"

    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(config_file))

    assert "is missing:\ta default config will be loaded" in caplog.text
    assert config.model_dump() == expected_default()


# ---------------------------------------------------------- PERMISSION ERROR
def test_file_unreadable(caplog: LogCaptureFixture, tmp_path: Path) -> None:
    """ Verify that parsing a file without reading permission
    logs the error and loads DEFAULT_CONFIG

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
    """
    config_file = tmp_path / "unreadable_file.json"
    config_file.write_text("anything in this file")
    config_file.chmod(0o000)

    try:
        with caplog.at_level(logging.WARNING):
            config = get_valid_config(str(config_file))

        assert "You have no permission to read" in caplog.text
        assert "a default config will be loaded" in caplog.text
        assert config.model_dump() == expected_default()

    finally:
        config_file.chmod(0o644)


# ---------------------------------------------------------------- FILE EMPTY
def test_file_empty(caplog: LogCaptureFixture, tmp_path: Path) -> None:
    """ Verify that parsing an empty file
    logs the error and loads DEFAULT_CONFIG

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
    """
    config_file = tmp_path / "empty_file.json"
    config_file.write_text("")

    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(config_file))

    assert "Config file has invalid syntax" in caplog.text
    assert "a default config will be loaded" in caplog.text
    assert config.model_dump() == expected_default()


# ===========================================================================
#                                                                    COMMENTS
# ===========================================================================

# -------------------------------------------------------- FILE with COMMENTS
@pytest.fixture
def json_with_comments() -> str:
    return """{
        # many levels
        "points_per_pacgum": 33, # starts without points
        // filename to save highscores
        "highscore_filename": "highscores.json",
        "lives": 33,
        "seed": 33, // WTF is that ?
        "level_max_time": 33
    }"""


def test_file_with_comments(tmp_path: Path,
                            json_with_comments: str) -> None:
    """ Verify that parsing a file with # or // comments
    succeed creating a config containing its valid values

    Args:
        tmp_path (Path): to build a path to a config file
        json_with_comments: a valid dict with additional comments
    """
    json_file = tmp_path / "file_with_comments.json"
    json_file.write_text(json_with_comments, encoding="utf-8")

    config = get_valid_config(str(json_file))

    assert config.points_per_pacgum == 33
    assert config.highscore_filename == resolved("highscores.json")
    assert config.lives == 33
    assert config.seed == 33
    assert config.level_max_time == 33


# ===========================================================================
#                                                                      SYNTAX
# ===========================================================================

# ------------------------------------------------------------- missing comma
@pytest.fixture
def json_without_comma() -> str:
    return """{
        "highscore_filename": "highscores.json",
        "lives": 33,
        "seed": 33
        "level_max_time": 33
    }"""


def test_invalid_json_syntax(caplog: LogCaptureFixture, tmp_path: Path,
                             json_without_comma: str) -> None:
    """ Verify that parsing a file with incorrect json format
    logs the error and loads DEFAULT_CONFIG

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_without_comma: a dict rendered invalid due to a missing comma
    """
    json_file = tmp_path / "incorrect_json_file.json"
    json_file.write_text(json_without_comma, encoding="utf-8")
    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(json_file))
    assert "Config file has invalid syntax" in caplog.text
    assert "a default config will be loaded" in caplog.text
    assert config.model_dump() == expected_default()


# ---------------------------------------------------------------- not a dict
@pytest.fixture
def json_no_dict() -> str:
    return """[
        "highscores.json",
        33,
        "seed",
        "level_max_time",
    ]"""


def test_json_not_a_dict(caplog: LogCaptureFixture, tmp_path: Path,
                         json_no_dict: str) -> None:
    """ Verify that parsing a file not containing a dict
    logs the error and loads DEFAULT_CONFIG

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_no_dict: a json invalid bacause not a dict
    """
    json_file = tmp_path / "incorrect_json_file.json"
    json_file.write_text(json_no_dict, encoding="utf-8")
    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(json_file))
    assert "Config file is not a dict" in caplog.text
    assert "a default config will be loaded" in caplog.text
    assert config.model_dump() == expected_default()


# ===========================================================================
#                                                             KEYS and VALUES
# ===========================================================================

# ------------------------------------------------------------------ bad keys
@pytest.fixture
def json_unknown_key() -> str:
    return """{
        "highscores": "highscores.json",
        "lives": 33
    }"""


def test_unexpected_keys_ignored(caplog: LogCaptureFixture, tmp_path: Path,
                                 json_unknown_key: str) -> None:
    """Verify that parsing a file with an unexpected key
    logs an info message and ignores this key

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_unknown_key: a valid json string with an unknown key
    """
    json_file = tmp_path / "unknown_key_file.json"
    json_file.write_text(json_unknown_key, encoding="utf-8")

    with caplog.at_level(logging.INFO):
        config = get_valid_config(str(json_file))

    assert "unknown keys ignored" in caplog.text
    assert config.highscore_filename == resolved(
        DEFAULT_CONFIG["highscore_filename"])
    assert config.lives == 33


# ------------------------------------------------------------------ bad type
@pytest.fixture
def json_wrong_type() -> str:
    return """{
        "seed": "not_int",
        "level_max_time": 33
    }"""


def test_invalid_type(caplog: LogCaptureFixture, tmp_path: Path,
                      json_wrong_type: str) -> None:
    """Verify that parsing a file with a wrong type for a value
    logs a warning message and replaces this value by the default one

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_wrong_type: a valid json string with a wrong value
    """
    json_file = tmp_path / "wrong_type.json"
    json_file.write_text(json_wrong_type, encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(json_file))

    assert "was invalid" in caplog.text
    assert config.seed == DEFAULT_CONFIG["seed"]
    assert config.level_max_time == 33


# -------------------------------------------------------------- out of range
@pytest.fixture
def json_out_of_range() -> str:
    return """{
        "lives": 0,
        "level_max_time": 33
    }"""


def test_out_of_range(caplog: LogCaptureFixture, tmp_path: Path,
                      json_out_of_range: str) -> None:
    """Verify that parsing a file with a value out of range
    logs a warning message and replaces this value by the default one

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_out_of_range: a valid json string with a value out of range
    """
    json_file = tmp_path / "out_of_range.json"
    json_file.write_text(json_out_of_range, encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(json_file))

    assert "was invalid" in caplog.text
    assert config.lives == DEFAULT_CONFIG["lives"]
    assert config.level_max_time == 33


# ----------------------------------------------------------------- bad regex
@pytest.fixture
def json_wrong_regex() -> str:
    return """{
        "highscore_filename": "invalid/name?.json",
        "level_max_time": 33
    }"""


def test_wrong_regex(caplog: LogCaptureFixture, tmp_path: Path,
                     json_wrong_regex: str) -> None:
    """Verify that parsing a file with a value that does not match the regex
    logs a warning message and replaces this value by the default one

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_wrong_regex: a valid json string with a non regex value
    """
    json_file = tmp_path / "wrong_regex.json"
    json_file.write_text(json_wrong_regex, encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(json_file))

    assert "was invalid" in caplog.text
    assert config.highscore_filename == resolved(
        DEFAULT_CONFIG["highscore_filename"])
    assert config.level_max_time == 33


# ===========================================================================
#                                                                      LEVELS
# ===========================================================================

# ------------------------------------------------------------------- bad ids
@pytest.fixture
def json_inconsistent_levels() -> str:
    return """{
        "level": [
            {"id": 22, "width": 12, "height": 12},
            {"id": 33, "width": 13, "height": 13},
            {"id": 33, "width": 14, "height": 14}
        ],
        "level_max_time": 33
    }"""


def test_add_missing_levels(caplog: LogCaptureFixture, tmp_path: Path,
                            json_inconsistent_levels: str) -> None:
    """Verify that parsing a file with inconsistent levels
    logs a warning message and replaces id levels by consecutives ids

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_inconsistent_levels: a valid json string with inconsistent levels
    """
    json_file = tmp_path / "json_wrong_levels.json"
    json_file.write_text(json_inconsistent_levels, encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(json_file))

    assert "replaced by" in caplog.text
    assert "levels found, padded to" in caplog.text
    assert len(config.level) == MIN_LEVELS
    assert config.level[0].id == 1
    assert config.level[0].width == 12
    assert config.level[0].height == 12
    assert config.level[1].id == 2
    assert config.level[2].id == 3
    assert config.level_max_time == 33


# ----------------------------------------------------------------- bad value
@pytest.fixture
def json_wrong_level_value() -> str:
    return """{
        "level": [
            {"id": 1, "width": 15, "height": 15},
            {"id": 2, "width": -13, "height": 13},
            {"id": 3, "width": 14, "height": 14},
            {"id": 4, "width": 15, "height": 15},
            {"id": 5, "width": 15, "height": 15},
            {"id": 6, "width": 15, "height": 15},
            {"id": 7, "width": 15, "height": 15},
            {"id": 8, "width": 15, "height": 15},
            {"id": 9, "width": 15, "height": 15},
            {"id": 10, "width": 15, "height": 15}
        ],
        "level_max_time": 33
    }"""


def test_wrong_value_in_level(caplog: LogCaptureFixture, tmp_path: Path,
                              json_wrong_level_value: str) -> None:
    """Verify that parsing a file with wrong level value
    logs a warning message and loads default value

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_wrong_level_value: a valid json string with wrong value in level
    """
    json_file = tmp_path / "json_wrong_levels.json"
    json_file.write_text(json_wrong_level_value, encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        config = get_valid_config(str(json_file))

    assert "Default value" in caplog.text
    assert "was invalid" in caplog.text
    assert config.level[1].id == 2
    assert config.level[1].width == DEFAULT_SIZE
    assert config.level[1].height == 13
    assert config.level_max_time == 33


# --------------------------------------------------------- wrong/missing key
@pytest.fixture
def json_wrong_level_key() -> str:
    return """{
        "level": [
            {"id": 1, "width": 15, "height": 15},
            {"id": 2, "width": 15, "height": 15},
            {"ids": 3, "width": 14, "height": 14},
            {"id": 4, "width": 15, "height": 15},
            {"id": 5, "width": 15, "height": 15},
            {"id": 6, "width": 15, "height": 15},
            {"id": 7, "width": 15, "height": 15},
            {"id": 8, "width": 15, "height": 15},
            {"id": 9, "width": 15, "height": 15},
            {"id": 10, "width": 15, "height": 15}
        ],
        "level_max_time": 33
    }"""


def test_wrong_key_in_level(caplog: LogCaptureFixture, tmp_path: Path,
                            json_wrong_level_key: str) -> None:
    """Verify that parsing a file with a wrong key in a level ignores it,
    logs messages, applies default for missing key, and auto-corrects if needed

    Args:
        caplog: to check the displayed message
        tmp_path (Path): to build a path to a config file
        json_wrong_level_key: a valid json string with wrong key in level
    """
    json_file = tmp_path / "json_wrong_levels.json"
    json_file.write_text(json_wrong_level_key, encoding="utf-8")

    with caplog.at_level(logging.INFO):
        config = get_valid_config(str(json_file))

    assert "LvlConfig" in caplog.text
    assert "unknown keys ignored: ids" in caplog.text
    assert "missing keys, defaults used: id" in caplog.text
    assert "Level id 1 replaced by 3" in caplog.text
    assert config.level[2].id == 3
    assert config.level[2].width == 14
    assert config.level[2].height == 14
    assert config.level_max_time == 33
