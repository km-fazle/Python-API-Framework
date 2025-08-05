.PHONY: help install test run clean docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=py_api_framework --cov-report=html

test-watch: ## Run tests in watch mode
	pytest-watch

lint: ## Run linting
	black py_api_framework tests
	flake8 py_api_framework tests
	mypy py_api_framework

format: ## Format code
	black py_api_framework tests

run: ## Run the application in development mode
	uvicorn py_api_framework.main:app --reload

run-prod: ## Run the application in production mode
	uvicorn py_api_framework.main:app --host 0.0.0.0 --port 8000

docker-build: ## Build Docker image
	docker build -t py-api-framework .

docker-run: ## Run with Docker Compose
	docker-compose up -d

docker-stop: ## Stop Docker Compose services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f *.db
	rm -f *.sqlite

setup: ## Initial setup
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "source venv/bin/activate  # On Unix/macOS"
	@echo "venv\\Scripts\\activate     # On Windows"

init-db: ## Initialize database
	python -c "from py_api_framework.database import init_db; init_db()"

check: ## Run all checks (lint, test)
	make lint
	make test 