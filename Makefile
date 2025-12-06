.PHONY: help install lint format check test clean all

# Default target
help:
	@echo "Available targets:"
	@echo "  make install     - Install dependencies using uv"
	@echo "  make lint        - Run all linters (ruff, mypy, yamllint, tombi)"
	@echo "  make format      - Auto-format all files (black, isort, ruff, tombi)"
	@echo "  make check       - Run linters without making changes"
	@echo "  make test        - Run tests with pytest"
	@echo "  make clean       - Remove build artifacts and cache files"
	@echo "  make all         - Format, lint, and test"

# Install dependencies
setup:
	uv sync --all-extras

# Linting targets
lint: lint-python lint-yaml lint-toml

lint-python:
	@echo "Running ruff linter..."
	uv run ruff check oeispy/ tests/
	@echo "Running mypy type checker..."
	uv run mypy oeispy/

lint-yaml:
	@echo "Linting YAML files..."
	uv run yamllint .github/

# Formatting targets
format: format-python format-toml

format-python:
	@echo "Sorting imports with isort..."
	uv run isort oeispy/ tests/
	@echo "Formatting with black..."
	uv run black oeispy/ tests/
	@echo "Auto-fixing with ruff..."
	uv run ruff check --fix oeispy/ tests/

format-toml:
	@echo "Formatting TOML files with tombi..."
	uv run tombi format pyproject.toml

# Check without modifications (for CI)
check: check-python check-yaml check-toml

check-python:
	@echo "Checking Python formatting..."
	uv run black --check oeispy/ tests/
	@echo "Checking import sorting..."
	uv run isort --check-only oeispy/ tests/
	@echo "Running ruff..."
	uv run ruff check oeispy/ tests/
	@echo "Running mypy..."
	uv run mypy oeispy/

check-yaml:
	@echo "Checking YAML files..."
	uv run yamllint .github/

lint-toml:
	@echo "Checking TOML files with tombi..."
	uv run tombi check pyproject.toml

check-toml:
	@echo "Checking TOML formatting..."
	uv run tombi check pyproject.toml

# Testing
test:
	@echo "Running pytest..."
	uv run pytest tests/

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

# Run everything
all: format lint test
