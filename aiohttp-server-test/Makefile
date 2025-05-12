.PHONY: setup lint format test docker-build docker-up docker-down docker-logs clean help benchmark

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[0;33m
NC=\033[0m # No Color

help: ## Show this help
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-15s$(NC) %s\n", $$1, $$2}'

setup: ## Install development dependencies
	@echo "$(YELLOW)Installing development dependencies...$(NC)"
	@if ! command -v uv &> /dev/null; then \
		echo "$(YELLOW)UV not found. Installing UV...$(NC)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	uv pip install -r requirements-dev.txt
	pre-commit install
	@echo "$(GREEN)Setup complete!$(NC)"

lint: ## Run all linters
	@echo "$(YELLOW)Running pre-commit checks on all files...$(NC)"
	pre-commit run --all-files

format: ## Format code with black and isort
	@echo "$(YELLOW)Formatting code...$(NC)"
	black .
	isort .
	@echo "$(GREEN)Formatting complete!$(NC)"

test: ## Run tests (add your test command here)
	@echo "$(YELLOW)Running tests...$(NC)"
	# Add your test command here (e.g., pytest)
	@echo "$(GREEN)Tests completed!$(NC)"

docker-build: ## Build all Docker containers
	@echo "$(YELLOW)Building Docker containers...$(NC)"
	docker compose build
	@echo "$(GREEN)Build complete!$(NC)"

docker-up: ## Start all Docker containers
	@echo "$(YELLOW)Starting Docker containers...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Containers are running!$(NC)"

docker-down: ## Stop all Docker containers
	@echo "$(YELLOW)Stopping Docker containers...$(NC)"
	docker compose down
	@echo "$(GREEN)Containers stopped!$(NC)"

docker-logs: ## View Docker container logs
	@echo "$(YELLOW)Showing Docker logs...$(NC)"
	docker compose logs -f

clean: ## Remove build artifacts and caches
	@echo "$(YELLOW)Cleaning project...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "$(GREEN)Clean complete!$(NC)"

benchmark: ## Run benchmarks for all server implementations
	@echo "$(YELLOW)Running benchmarks...$(NC)"
	@echo "Benchmarking simple server on port 8080..."
	@if ! command -v hey &> /dev/null; then \
		echo "$(YELLOW)'hey' not found. Please install it first: go install github.com/rakyll/hey@latest$(NC)"; \
		exit 1; \
	fi
	hey -n 10000 -c 100 http://localhost:8080/
	@echo "\nBenchmarking gunicorn server on port 8081..."
	hey -n 10000 -c 100 http://localhost:8081/
	@echo "\nBenchmarking gunicorn-uvloop server on port 8082..."
	hey -n 10000 -c 100 http://localhost:8082/
	@echo "$(GREEN)Benchmarks complete!$(NC)"

venv: ## Create a virtual environment using UV
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	@if ! command -v uv &> /dev/null; then \
		echo "$(YELLOW)UV not found. Installing UV...$(NC)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	uv venv
	@echo "$(GREEN)Virtual environment created! Activate it with 'source .venv/bin/activate'$(NC)"
