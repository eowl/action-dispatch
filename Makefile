.PHONY: help install test lint format type-check clean build upload-test upload

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	python -m unittest discover tests -v

test-coverage:  ## Run tests with coverage
	coverage run -m unittest discover tests
	coverage report
	coverage html

lint:  ## Run linting
	flake8 action_dispatch tests

format:  ## Format code
	black action_dispatch tests

format-check:  ## Check code formatting
	black --check action_dispatch tests

type-check:  ## Run type checking
	mypy action_dispatch

check-all: format-check lint type-check test  ## Run all checks

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

upload-test:  ## Upload to TestPyPI
	python -m twine upload --repository testpypi dist/*

upload:  ## Upload to PyPI
	python -m twine upload dist/*

setup-dev:  ## Set up development environment
	pip install -e ".[dev]"
	pre-commit install
