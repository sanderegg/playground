#!/usr/bin/env python3

import multiprocessing

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "aiohttp.GunicornWebWorker"
accesslog = "-"
errorlog = "-"
