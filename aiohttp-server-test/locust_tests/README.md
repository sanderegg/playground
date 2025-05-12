# AIOHTTP Server Benchmark with Locust

This directory contains Locust load testing configurations for benchmarking the three AIOHTTP server implementations:

1. Simple AIOHTTP server (port 8080)
2. Gunicorn with AIOHTTP workers (port 8081)
3. Gunicorn with AIOHTTP workers and uvloop (port 8082)

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or use the project's UV setup:

```bash
cd ..
make venv
source .venv/bin/activate
cd locust_tests
pip install -r requirements.txt
```

## Running Tests

### Option 1: Using the Web UI

Start the Locust web interface:

```bash
locust -f locustfile.py
```

Then open your browser at http://localhost:8089/ to configure and run tests.

### Option 2: Using the Command-Line Script

For headless testing with automatic result saving:

```bash
python run_tests.py
```

You can customize the test parameters:

```bash
python run_tests.py --time 120 --users 200 --spawn-rate 20
```

## Understanding Results

After running tests, check the `results` directory for:

- CSV files with detailed metrics
- HTML report with graphs and statistics

Key metrics to compare:
- Requests per second (RPS)
- Response time (min, avg, median, max)
- Failure rate

## Adding to Makefile

You can add the following to the project's Makefile for easy access:

```makefile
locust-test: ## Run Locust load tests on all server implementations
	@echo "$(YELLOW)Running Locust load tests...$(NC)"
	cd locust_tests && python run_tests.py
	@echo "$(GREEN)Load tests complete!$(NC)"
```
