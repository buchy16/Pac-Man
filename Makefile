LOCK = uv.lock
PYTHON = python3 -m

all : run

.venv/bin/activate : 
	$(PYTHON) uv sync

$(LOCK) :
	$(PYTHON) uv sync

install : .venv/bin/activate $(LOCK)

run : install
	$(PYTHON) uv run python -m src

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

uninstall : install
	rm -rf .venv
	rm -rf $(LOCK)

.PHONY: clean lint run install uninstall