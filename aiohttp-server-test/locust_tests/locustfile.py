#!/usr/bin/env python3
"""
Simple Locust test file for benchmarking AIOHTTP server implementations.

This file defines user behaviors for testing the three different AIOHTTP server implementations:
- Simple AIOHTTP server (port 8080)
- Gunicorn with AIOHTTP workers (port 8081)
- Gunicorn with AIOHTTP workers and uvloop (port 8082)

Tests only the root endpoint (/) for simplicity.
"""

import socket

from locust import FastHttpUser, task


# Get local IP address dynamically
def get_local_ip():
    try:
        # Create a socket connection to an external server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't actually connect but gives us the IP that would be used
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback to localhost if unable to determine IP
        return "localhost"


# Local IP address to be used for all hosts
LOCAL_IP = get_local_ip()


class RootCallUser(FastHttpUser):

    @task
    def get_root(self):
        """Test the root endpoint (/)."""
        self.client.get("/", name="Root")
