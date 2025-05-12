#!/usr/bin/env python3

# Install uvloop as the default event loop
import asyncio
import multiprocessing

import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "aiohttp.GunicornWebWorker"
accesslog = "-"
errorlog = "-"
