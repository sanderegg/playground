.PHONY: setup lint format test docker-build docker-up docker-down docker-logs clean help benchmark locust-test locust-web max-rps

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[0;33m
RED=\033[0;31m
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

build: ## Build all Docker containers
	@echo "$(YELLOW)Building Docker containers...$(NC)"
	docker compose build
	@echo "$(GREEN)Build complete!$(NC)"

up: ## Start all Docker containers
	@echo "$(YELLOW)Starting Docker containers...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Containers are running!$(NC)"

down: ## Stop all Docker containers
	@echo "$(YELLOW)Stopping Docker containers...$(NC)"
	docker compose down
	@echo "$(GREEN)Containers stopped!$(NC)"

logs: ## View Docker container logs
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

	hey -n 10000 -c 100 http://localhost:8080/
	@echo "\nBenchmarking gunicorn server on port 8081..."
	hey -n 10000 -c 100 http://localhost:8081/
	@echo "\nBenchmarking gunicorn-uvloop server on port 8082..."
	hey -n 10000 -c 100 http://localhost:8082/
	@echo "$(GREEN)Benchmarks complete!$(NC)"

locust-test: ## Run Locust load tests on all server implementations
	@echo "$(YELLOW)Running Locust load tests...$(NC)"
	cd locust_tests && ./compare_servers.sh
	@echo "$(GREEN)Load tests complete! Check locust_tests/results for detailed reports.$(NC)"

locust-web: ## Run Locust with web UI for interactive load testing
	@echo "$(YELLOW)Starting Locust web interface...$(NC)"
	@IP=$$(hostname -I | awk '{print $$1}'); \
	echo "$(YELLOW)Detected local IP: $$IP$(NC)"; \
	echo "$(YELLOW)Open http://localhost:8089/ in your browser to run tests.$(NC)"; \
	echo "$(YELLOW)Host field will be prefilled with http://$$IP:8080$(NC)"; \
	cd locust_tests && locust --processes 4 --host="http://$$IP:8080" -f locustfile.py

max-rps: ## Find maximum sustainable request rate for all server implementations
	@echo "$(YELLOW)Finding maximum sustainable request rate for all servers...$(NC)"
	cd locust_tests && ./find_max_rps.py
	@echo "$(GREEN)Test complete! Check locust_tests/results/max_rps_* directory for results.$(NC)"

venv: ## Create a virtual environment using UV
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	@if ! command -v uv &> /dev/null; then \
		echo "$(YELLOW)UV not found. Installing UV...$(NC)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	uv venv
	@echo "$(GREEN)Virtual environment created! Activate it with 'source .venv/bin/activate'$(NC)"
