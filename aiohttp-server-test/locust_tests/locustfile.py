#!/usr/bin/env python3
"""
Simple Locust test file for benchmarking AIOHTTP server implementations.

This file defines user behaviors for testing the three different AIOHTTP server implementations:
- Simple AIOHTTP server (port 8080)
- Gunicorn with AIOHTTP workers (port 8081)
- Gunicorn with AIOHTTP workers and uvloop (port 8082)

Tests only the root endpoint (/) for simplicity.
"""

from locust import HttpUser, between, task


class SimpleServerUser(HttpUser):
    """User that tests the simple AIOHTTP server on port 8080."""

    host = "http://localhost:8080"
    wait_time = between(0.1, 0.3)  # Wait between 100ms and 300ms between tasks

    @task
    def get_root(self):
        """Test the root endpoint (/)."""
        self.client.get("/", name="Simple Server - Root")


class GunicornServerUser(HttpUser):
    """User that tests the Gunicorn AIOHTTP server on port 8081."""

    host = "http://localhost:8081"
    wait_time = between(0.1, 0.3)  # Wait between 100ms and 300ms between tasks

    @task
    def get_root(self):
        """Test the root endpoint (/)."""
        self.client.get("/", name="Gunicorn Server - Root")


class GunicornUvloopServerUser(HttpUser):
    """User that tests the Gunicorn AIOHTTP server with uvloop on port 8082."""

    host = "http://localhost:8082"
    wait_time = between(0.1, 0.3)  # Wait between 100ms and 300ms between tasks

    @task
    def get_root(self):
        """Test the root endpoint (/)."""
        self.client.get("/", name="Gunicorn+uvloop Server - Root")
