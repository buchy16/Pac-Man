# Ajouté dans Makefile :
# test:
# 	uv run pytest tests/


import json
from pathlib import Path
from typing import Any

import commentjson
import pytest
from pydantic import ValidationError

from src.parse_config import (GameConfig, parse_validate_config, parsing)

# ===========================================================================
#                                            DICTIONNAIRE VALIDE de référence
# ===========================================================================

@pytest.fixture
def valid_config_dict() -> dict[str, Any]:
    """Provide a minimal, valid game configuration dictionary.

    Returns:
        dict[str, Any]: A dictionary that, once serialized to JSON,
        parses and validates successfully via ``parse_validate_config``.
    """
    return {
        "highscore_filename": "highscores.json",
        "level": [
            {"id": i, "width": 15, "height": 15} for i in range(1, 11)
        ],
        "lives": 3,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
        "level_max_time": 90,
    }

# autre fixture : `tmp_path`
# Pour tester `parse_config`, il faut créer des fichiers `config.txt` factices
# avec du contenu volontairement invalide... mais sans polluer l'espace disque.
# => Pytest fournit une fixture toute prête pour ça : à chaque test `tmp_path`
# crée un dossier temporaire unique, automatiquement nettoyé après :D

# ===========================================================================
#                                                              FILE NOT FOUND
# ===========================================================================

def test_file_not_found(tmp_path: Path) -> None:
    """Verify that parsing a missing file raises `FileNotFoundError`.

    Args:
        tmp_path (Path): to build a path to a config file that is never created
    """

    config_file = tmp_path / "config.json"

    with pytest.raises(FileNotFoundError):
        parse_validate_config(config_file)


# ===========================================================================
#                                                              INVALID SYNTAX
# ===========================================================================

# ---------------------------------------------------------------------------
#                                                                  EMPTY FILE
# ---------------------------------------------------------------------------
def test_empty_file(tmp_path: Path) -> None:
    """Verify that an empty file raises a `JSONLibraryException`.
    (empty file is not valid JSON = syntax error)

    Args:
        tmp_path (Path): to create the empty config file
    """
    config_file = tmp_path / "config.json"
    config_file.write_text("")

    with pytest.raises(commentjson.JSONLibraryException):
        parse_validate_config(config_file)

# ---------------------------------------------------------------------------
#                                                             INVALID CONTENT
# ---------------------------------------------------------------------------
def test_invalid_json_syntax(tmp_path: Path) -> None:
    """Verify that malformed JSON content raises a `JSONLibraryException`.

    Args:
        tmp_path (Path): to create the malformed config file.
    """
    config_file = tmp_path / "config.json"
    config_file.write_text("{ not valid json ")

    with pytest.raises(commentjson.JSONLibraryException):
        parse_validate_config(config_file)


# ===========================================================================
#                                                               PYDANTIC FAIL
# ===========================================================================

# ---------------------------------------------------------------------------
#                                                    Invalid number of levels
# ---------------------------------------------------------------------------
def test_no_levels(tmp_path: Path,
                          valid_config_dict: dict[str, Any]) -> None:
    """Verify that no level failing Pydantic validation 
    raises a ``ValidationError``.

    Args:
        tmp_path (Path): to create the config file.
        valid_config_dict (dict[str, Any]): the valid config fixture.
    """
    valid_config_dict["level"] = []  # violates "at least one level"
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(valid_config_dict))

    with pytest.raises(ValidationError, match="The game requires at least ten levels"):
        parse_validate_config(config_file)


# ===========================================================================
#                                                               COMMENTS FAIL
# ===========================================================================

# ---------------------------------------------------------------------------
#                                                         hash style comments
# ---------------------------------------------------------------------------
def test_hash_comments(tmp_path: Path,
                               valid_config_dict: dict[str, Any]) -> None:
    """Verify that ``#``-style comments in the file do NOT break parsing.

    Args:
        tmp_path (Path): to create the config file.
        valid_config_dict (dict[str, Any]): the valid config fixture.
    """
    raw = json.dumps(valid_config_dict, indent=2)
    commented = "# a leading comment\n" + raw.replace(
        '"lives": 3,', '"lives": 3, # an inline comment\n'
    )
    config_file = tmp_path / "config.json"
    config_file.write_text(commented)

    config = parse_validate_config(config_file)

    assert isinstance(config, GameConfig)
    assert config.lives == 3

# ---------------------------------------------------------------------------
#                                                        slash style comments
# ---------------------------------------------------------------------------
def test_slash_comments(tmp_path: Path,
                                valid_config_dict: dict[str, Any]) -> None:
    """Verify that ``//``-style comments in the file do NOT break parsing.

    Args:
        tmp_path (Path): to create the config file.
        valid_config_dict (dict[str, Any]): the valid config fixture.
    """
    raw = json.dumps(valid_config_dict, indent=2)
    commented = "// a leading comment\n" + raw.replace(
        '"seed": 42,', '"seed": 42, // inline comment\n'
    )
    config_file = tmp_path / "config.json"
    config_file.write_text(commented)

    config = parse_validate_config(config_file)

    assert isinstance(config, GameConfig)
    assert config.seed == 42