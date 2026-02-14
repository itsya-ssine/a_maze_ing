PYTHON := python3
MAIN := a_maze_ing.py
CONFIG := config.txt
VENV := .venv

PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python3
MYPY := $(VENV)/bin/mypy
FLAKE8 := $(VENV)/bin/flake8

.PHONY: install run debug clean lint lint-strict

# Install project dependencies
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy

# Run the main program
run:
	$(PY) $(MAIN) $(CONFIG)

# Run the program in debug mode (pdb)
debug:
	$(PY) -m pdb $(MAIN) $(CONFIG)

# Remove temporary and cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .coverage $(VENV)

# Mandatory linting rules
lint:
	$(FLAKE8) --exclude=$(VENV) .
	$(MYPY) --exclude $(VENV) . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

# Optional strict linting
lint-strict:
	$(FLAKE8) --exclude=$(VENV) .
	$(MYPY) --exclude $(VENV) . --strict
