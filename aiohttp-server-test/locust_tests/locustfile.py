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

    @task
    def get_v0_entrypoint(self) -> None:
        self.client.get("/v0/", name="v0", auth=_AUTH)

    @task(10)
    def get_auth_check(self) -> None:
        self.client.get("/v0/auth:check", name="auth-check", auth=_AUTH)

    def on_start(self) -> None:
        response = self.client.post(
            "/v0/auth/login",
            json={
                "email": os.environ.get("OSPARC_USERNAME"),
                "password": os.environ.get("OSPARC_PASSWORD"),
            },
            name="auth-login",
            auth=_AUTH,
        )
        response.raise_for_status()

    def on_stop(self) -> None:
        self.client.post("/v0/auth/logout", name="auth-logout", auth=_AUTH)
