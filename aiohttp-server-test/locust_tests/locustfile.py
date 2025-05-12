#!/usr/bin/env python3
"""
Locust test file for benchmarking AIOHTTP server implementations.

This file defines user behaviors for testing the three different AIOHTTP server implementations:
- Simple AIOHTTP server (port 8080)
- Gunicorn with AIOHTTP workers (port 8081)
- Gunicorn with AIOHTTP workers and uvloop (port 8082)
"""

import random
from typing import List

from locust import HttpUser, TaskSet, between, task


class BaseServerBehavior(TaskSet):
    """Base behavior for testing any of the server implementations."""

    # List of names to use in the /{name} endpoint test
    names: List[str] = [
        "Alice",
        "Bob",
        "Charlie",
        "Dave",
        "Eve",
        "Frank",
        "Grace",
        "Heidi",
    ]

    @task(3)
    def get_root(self) -> None:
        """Test the root endpoint (/)."""
        with self.client.get("/", name=f"{self.base_name} - Root Endpoint") as response:
            if response.status_code != 200:
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def get_with_name(self) -> None:
        """Test the /{name} endpoint with random names."""
        name = random.choice(self.names)
        with self.client.get(
            f"/{name}", name=f"{self.base_name} - Named Endpoint"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Got status code {response.status_code}")

    @task(1)
    def get_health(self) -> None:
        """Test the health check endpoint."""
        with self.client.get(
            "/health", name=f"{self.base_name} - Health Check"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Got status code {response.status_code}")


class SimpleServerUser(HttpUser):
    """User that tests the simple AIOHTTP server on port 8080."""

    host = "http://localhost:8080"
    wait_time = between(0.1, 0.5)  # Wait between 100ms and 500ms between tasks

    class SimpleServerBehavior(BaseServerBehavior):
        base_name = "Simple Server"

    tasks = [SimpleServerBehavior]


class GunicornServerUser(HttpUser):
    """User that tests the Gunicorn AIOHTTP server on port 8081."""

    host = "http://localhost:8081"
    wait_time = between(0.1, 0.5)  # Wait between 100ms and 500ms between tasks

    class GunicornServerBehavior(BaseServerBehavior):
        base_name = "Gunicorn Server"

    tasks = [GunicornServerBehavior]


class GunicornUvloopServerUser(HttpUser):
    """User that tests the Gunicorn AIOHTTP server with uvloop on port 8082."""

    host = "http://localhost:8082"
    wait_time = between(0.1, 0.5)  # Wait between 100ms and 500ms between tasks

    class GunicornUvloopServerBehavior(BaseServerBehavior):
        base_name = "Gunicorn+uvloop Server"

    tasks = [GunicornUvloopServerBehavior]
