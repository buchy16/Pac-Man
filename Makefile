MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
# Allows to run `make run CONFIG=other_config.json` without modifying the Makefile :D
CONFIG ?= src/data/config.json

all: install run

install:
	uv sync

update:
	uv lock --upgrade
	uv sync

test:
	uv run pytest tests/

run:
	uv run python pac-man.py $(CONFIG)

debug:
	uv run python -m pdb pac-man.py src $(CONFIG)

lint:
	uv run flake8 src
	uv run mypy src $(MYPY_FLAGS)

lint-strict:
	uv run flake8 src
	uv run mypy --strict src $(MYPY_FLAGS)

package:
	uv run --no-dev --group build pyinstaller PacMan.spec --noconfirm --clean

clean:
	rm -rf .mypy_cache .pytest_cache build dist
	@find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	rm -rf .venv

.PHONY: all install update test run debug lint lint-strict package clean fclean