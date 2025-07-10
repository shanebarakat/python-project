.PHONY: help install test lint run

# Variables
PYTHON = python3
VENV_DIR = .venv
VENV_ACTIVATE = . $(VENV_DIR)/bin/activate

help:
	@echo "Commands:"
	@echo "  install    : Create virtual environment and install dependencies."
	@echo "  test       : Run tests."
	@echo "  lint       : Run linter and formatter."
	@echo "  run        : Run the main application."

install:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo ">>> Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@echo ">>> Installing dependencies..."
	@$(VENV_ACTIVATE); \
	pip install --upgrade pip; \
	pip install -e ".[dev]"

test:
	@echo ">>> Running tests..."
	@$(VENV_ACTIVATE); \
	pytest

lint:
	@echo ">>> Running linter and formatter..."
	@$(VENV_ACTIVATE); \
	ruff check . && ruff format .

run:
	@echo ">>> Running application..."
	@$(VENV_ACTIVATE); \
	hello 