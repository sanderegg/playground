#!/bin/bash
# Script to run a comparison test against all three server implementations

# Make sure all three servers are running
echo "Checking if all three servers are running..."

# Check simple server (port 8080)
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo "Error: Simple server not running on port 8080!"
    echo "Please start all servers with 'make docker-up' before running this test."
    exit 1
fi

# Check gunicorn server (port 8081)
if ! curl -s http://localhost:8081/health > /dev/null; then
    echo "Error: Gunicorn server not running on port 8081!"
    echo "Please start all servers with 'make docker-up' before running this test."
    exit 1
fi

# Check gunicorn-uvloop server (port 8082)
if ! curl -s http://localhost:8082/health > /dev/null; then
    echo "Error: Gunicorn+uvloop server not running on port 8082!"
    echo "Please start all servers with 'make docker-up' before running this test."
    exit 1
fi

echo "All servers are running. Starting Locust tests..."

# Run the Python script with provided arguments
cd "$(dirname "$0")"
python run_tests.py "$@"
