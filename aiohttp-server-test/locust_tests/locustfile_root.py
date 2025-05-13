#!/usr/bin/env python3
"""
Simple Locust test file for benchmarking AIOHTTP server implementations.
"""

import os

from locust import HttpUser, task

_AUTH = (os.environ.get("SC_USER_NAME"), os.environ.get("SC_USER_PASSWORD"))


class RootCallUser(HttpUser):

    @task
    def get_root(self) -> None:
        self.client.get("/", name="Root", auth=_AUTH)
