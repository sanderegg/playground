# filepath: /home/anderegg/dev/github/playground/aiohttp-server-test/gunicorn_uvloop/uvloop_server.py
#!/usr/bin/env python3

from aiohttp import web


async def handle(request):
    name = request.match_info.get("name", "Anonymous")
    return web.Response(
        text=f"Hello, {name} from gunicorn with aiohttp workers and uvloop!"
    )


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
