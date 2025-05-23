#!/usr/bin/env python3

import multiprocessing
import os
import sys

bind = "0.0.0.0:8080"
cpu_count = multiprocessing.cpu_count()
# Use CPU_LIMIT env var if set, otherwise use detected CPUs
cpu_limit = int(os.environ.get("CPU_LIMIT", cpu_count))
workers = 1  # cpu_limit * 2 + 1

# Print CPU and worker information at startup
print(f"CPUs detected: {cpu_count}", file=sys.stderr)
print(f"CPU limit set to: {cpu_limit}", file=sys.stderr)
print(f"Setting {workers} worker processes", file=sys.stderr)

worker_class = "aiohttp.GunicornWebWorker"
accesslog = "-"
errorlog = "-"
reload = True
worker_tmp_dir = "/dev/shm"
