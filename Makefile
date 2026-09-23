# factorisé les flags dupliqués
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
# permet `make run CONFIG=level2.json` sans toucher au Makefile :D
CONFIG ?= config.json

all: install run

install:
	@# uv sync est TRES intelligent :P
	@# il lit aveuglément le lockfile (uv.lock) existant,
	@# crée le .venv s'il est absent,
	@# y installe exactement les dépendances issues du `pyproject.toml`.
	uv sync

update:
	@# pour forcer la mise à jour de uv.lock si il y a eu modif manuelle
	@# des dépendances dans pyproject.toml
	uv lock --upgrade
	uv sync

test:
	uv run pytest tests/

run:
	uv run python -m src $(CONFIG)

debug:
	uv run python -m pdb -m src config.json

lint:
	uv run flake8 src
	uv run mypy src $(MYPY_FLAGS)

lint-strict:
	uv run flake8 src
	uv run mypy --strict src $(MYPY_FLAGS)

# Pour le packaging, penser à utiliser le flag --no-dev
package:
	uv sync --no-dev
	# commande de packaging

# supprime tout ce qui est régénérable automatiquement
clean:
	rm -rf .mypy_cache .pytest_cache build dist
	@find . -type d -name "__pycache__" -exec rm -rf {} +

# supprime en plus ce qui nécessite une action manuelle pour être reconstruit
fclean: clean
	rm -rf .venv uv.lock

.PHONY: all install update test run debug lint lint-strict clean fclean