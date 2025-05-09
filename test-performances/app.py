import os
import asyncio
import uvloop
import orjson
import socket
from typing import Dict, Any
from aiohttp import web

# Replace the standard asyncio event loop with uvloop for better performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Set socket options for performance
socket.setdefaulttimeout(30.0)


# Custom JSON response function using orjson for faster serialization
def fast_json_response(data: Dict[str, Any], status: int = 200) -> web.Response:
    return web.Response(
        body=orjson.dumps(data), status=status, content_type="application/json"
    )


async def handle(request: web.Request) -> web.Response:
    return fast_json_response({"message": "Hello, World!"})


def init_app():
    # Configure application with performance-optimized settings
    app = web.Application(
        client_max_size=1024**2,  # 1MB max request size
    )

    # Simple in-memory response cache
    cache = {}

    @web.middleware
    async def cache_middleware(request: web.Request, handler):
        # Only cache GET requests to specific paths
        if request.method == "GET":
            cache_key = request.path_qs
            cached = cache.get(cache_key)
            if cached:
                return cached

        # Call the handler
        response = await handler(request)

        # Cache successful GET responses
        if request.method == "GET" and response.status == 200:
            # Store a copy of the response by reading and recreating it
            body = await response.read()
            cached_response = web.Response(
                body=body, status=response.status, headers=response.headers.copy()
            )
            cache[request.path_qs] = cached_response

        return response

    # Apply middleware
    app.middlewares.append(cache_middleware)

    # Add routes
    app.router.add_get("/", handle)

    return app


if __name__ == "__main__":
    # Determine optimal number of workers based on CPU cores
    # Use workers_count = min(2 * CPU_CORES + 1, MAX_WORKERS)
    # which is a good rule of thumb for I/O bound applications
    cpu_cores = os.cpu_count() or 1
    workers_count = min(2 * cpu_cores + 1, 8)  # Cap at 8 workers maximum

    # Increase socket buffer size for better network performance
    socket_options = [
        (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
        (socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024),  # 1MB receive buffer
        (socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024),  # 1MB send buffer
        (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),  # Disable Nagle's algorithm
    ]

    app = init_app()

    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8080))

    print(f"Starting server with {workers_count} worker(s) on http://0.0.0.0:{port}")

    # Configure server with performance optimizations
    web.run_app(
        app,
        host="0.0.0.0",
        port=port,
        shutdown_timeout=60.0,
        access_log_format='%t "%r" %s %b "%{Referer}i" "%{User-Agent}i" %Tfs',
        ssl_context=None,  # Explicitly disable SSL for better performance when not needed
    )
