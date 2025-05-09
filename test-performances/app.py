import os
import asyncio
import uvloop
import orjson
import socket
import time
from typing import Dict, Any, Callable, Awaitable, Optional
from aiohttp import web

# Replace the standard asyncio event loop with uvloop for better performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Custom JSON response function using orjson for faster serialization
def fast_json_response(data: Dict[str, Any], status: int = 200) -> web.Response:
    return web.Response(
        body=orjson.dumps(data),
        status=status,
        content_type="application/json"
    )

async def handle(request: web.Request) -> web.Response:
    return fast_json_response({"message": "Hello, World!"})

def init_app():
    # Configure application with performance-optimized settings
    app = web.Application(
        client_max_size=1024**2,  # 1MB max request size
        # keepalive_timeout=75.0,   # Keepalive timeout
        # compress=True             # Enable response compression
    )
    
    
    
    
    # Add routes
    app.router.add_get('/', handle)
    
    return app

if __name__ == '__main__':
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
    
    print(f"Starting server with {workers_count} worker(s) on http://0.0.0.0:8080")
    
    # Configure server with performance optimizations
    web.run_app(
        app,
        host='0.0.0.0',
        port=8080,
        shutdown_timeout=60.0,
        # keepalive_timeout=75.0,
        # tcp_keepalive=True,
        access_log_format='%t "%r" %s %b "%{Referer}i" "%{User-Agent}i" %Tfs',
        ssl_context=None,  # Explicitly disable SSL for better performance when not needed
        # socket_options=socket_options  # Apply custom socket options
    )
