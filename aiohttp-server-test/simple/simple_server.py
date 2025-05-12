# filepath: /home/anderegg/dev/github/playground/aiohttp-server-test/simple/simple_server.py
#!/usr/bin/env python3

import multiprocessing
import sys

from aiohttp import web


async def handle(request):
    name = request.match_info.get("name", "Anonymous")
    return web.Response(text=f"Hello, {name} from simple aiohttp server!")


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
    return app


app = create_app()

if __name__ == "__main__":
    cpu_count = multiprocessing.cpu_count()
    print(f"CPUs detected: {cpu_count}", file=sys.stderr)
    print("Simple server running with 1 process", file=sys.stderr)
    web.run_app(app, host="0.0.0.0", port=8080)
