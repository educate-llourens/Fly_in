MAIN= src/__main__.py
VENV_DIR= .venv
BIN_DIR= $(VENV_DIR)/bin
PYTHON= $(BIN_DIR)/python3
PIP= $(BIN_DIR)/pip
ACTIVATE=$(BIN_DIR)activate
MAP ?= maps/01_linear_path.txt
MYPY_FLAGS= --warn-return-any \
			--warn-unused-ignore \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs

all: run

install:
	uv venv
	uv sync
run:
	uv run python3 -m src $(MAP)

debug:
	$(PYTHON) -m pdb $(MAIN) $(MAP)

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache

bonfire:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache

lint:
	uv run flake8 --exclude=.venv,testing
	uv run mypy --exclude '.venv/|testing . $(MYPY_FLAGS)

lint-strict:
	uv run flake8 --exclude=.venv,testing
	uv run mypy --exclude '.venv/|testing/' . $(MYPY_FLAGS)