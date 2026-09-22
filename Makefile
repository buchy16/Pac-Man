LOCK = uv.lock
PYTHON = python3 -m

all : run

run :
	uv run python -m src

update:
	uv lock --upgrade
	uv sync --group app

lint : install
	. ./.venv/bin/activate && \
	flake8 src && \
	mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict : install
	. ./.venv/bin/activate && \
	flake8 src && \
	mypy --strict src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean : 
	find . -name "__pycache__" -exec rm -rf {} \+
	find . -name ".mypy_cache" -exec rm -rf {} \+
	find . -name ".vscode" -exec rm -rf {} \+

uninstall :
	rm -rf .venv
	rm -rf $(LOCK)

.PHONY: clean lint run install uninstall