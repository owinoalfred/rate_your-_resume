# Variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/Scripts/python.exe
PIP = $(VENV_DIR)/Scripts/pip.exe
STREAMLIT = $(VENV_DIR)/Scripts/streamlit.exe

# Default target
.PHONY: all
all: help

# Help message
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make venv          - Create a virtual environment"
	@echo "  make install       - Install dependencies"
	@echo "  make run           - Run the Streamlit app"
	@echo "  make clean         - Remove virtual environment and caches"
	@echo "  make git-push      - Commit and push changes to Git"
	@echo "  make lint          - Lint and format the code"
	@echo "  make test          - Run tests"

# Create virtual environment
.PHONY: venv
venv:
	@echo Creating virtual environment...
	python -m venv $(VENV_DIR)

# Install dependencies (just install from requirements.txt)
.PHONY: install
install:
	@echo Installing dependencies...
	$(PIP) install -r requirements.txt

# Run the Streamlit app (doesn't check anything, just runs it)
.PHONY: run
run:
	@echo Starting the Streamlit app...
	$(STREAMLIT) run app.py

# Remove virtual environment and caches
.PHONY: clean
clean:
	@echo Removing virtual environment and cache files...
	rmdir /S /Q $(VENV_DIR)
	for /d %%d in (__pycache__) do rmdir /S /Q "%%d"
	for %%f in (*.pyc) do del "%%f"

# Git commands
.PHONY: git-push
git-push:
	@echo Committing and pushing changes to Git...
	./auto_push.sh

# Lint the code
.PHONY: lint
lint:
	@echo Checking code quality and formatting...
	$(PIP) install black flake8
	$(PYTHON) -m black .
	$(PYTHON) -m flake8 .

# Run tests
.PHONY: test
test:
	@echo Running tests...
	$(PIP) install pytest
	$(PYTHON) -m pytest tests/