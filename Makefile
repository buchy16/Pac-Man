MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
# permet `make run CONFIG=level2.json` sans toucher au Makefile :D
CONFIG ?= config.json

all: install run

install:
	uv sync

update:
	uv lock --upgrade
	uv sync

test:
	uv run pytest tests/

run:
	uv run python -m src $(CONFIG)

debug:
	uv run python -m pdb -m src $(CONFIG)

lint:
	uv run flake8 src
	uv run mypy src $(MYPY_FLAGS)

lint-strict:
	uv run flake8 src
	uv run mypy --strict src $(MYPY_FLAGS)

package:
	uv sync --no-dev
	# commande de packaging

clean:
	rm -rf .mypy_cache .pytest_cache build dist
	@find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	rm -rf .venv uv.lock

.PHONY: all install update test run debug lint lint-strict package clean fclean