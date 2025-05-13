#!/usr/bin/env python3

import asyncio
import logging

from aiohttp import web

_logger = logging.getLogger(__name__)


async def handle(request):
    await asyncio.sleep(0)  # Simulate some processing delay
    name = request.match_info.get("name", "Anonymous")
    return web.Response(text=f"Hello, {name} from aiohttp!")


async def health_check(request):
    return web.Response(text="OK")


def create_app():
    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle),
            web.get("/health", health_check),
            web.get("/{name}", handle),
        ]
    )
    _logger.info("Aiohttp app created")
    return app


app = create_app()


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
