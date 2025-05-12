#!/usr/bin/env python3
"""
Script to run Locust tests against all three server implementations simultaneously.
This provides a headless mode alternative to the Locust web UI.
"""

import argparse
import csv
import os
import subprocess
from datetime import datetime
from pathlib import Path


def run_locust_test(
    test_time: int = 60, users: int = 100, spawn_rate: int = 10
) -> None:
    """
    Run Locust tests against all three server implementations.

    Args:
        test_time: Duration of the test in seconds
        users: Number of users to simulate
        spawn_rate: Rate at which to spawn users per second
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / "results" / timestamp
    os.makedirs(results_dir, exist_ok=True)

    print(f"Starting Locust tests - results will be saved to {results_dir}")

    cmd = [
        "locust",
        "--headless",
        "--users",
        str(users),
        "--spawn-rate",
        str(spawn_rate),
        "--run-time",
        f"{test_time}s",
        "--csv",
        str(results_dir / "stats"),
        "--csv-full-history",
        "--html",
        str(results_dir / "report.html"),
        "-f",
        str(Path(__file__).parent / "locustfile.py"),
    ]

    subprocess.run(cmd, check=True)

    print(f"\nTest completed. Results saved to {results_dir}")
    print(f"HTML report: {results_dir / 'report.html'}")

    # Print a quick summary of the results
    print("\nQuick Summary:")
    stats_csv = results_dir / "stats_stats.csv"
    if stats_csv.exists():
        with open(stats_csv, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            for row in rows:
                name = row.get("Name", "Unknown")
                requests = row.get("Request Count", "0")
                failures = row.get("Failure Count", "0")
                median = row.get("Median Response Time", "0")
                avg = row.get("Average Response Time", "0")
                min_rt = row.get("Min Response Time", "0")
                max_rt = row.get("Max Response Time", "0")
                rps = row.get("Requests/s", "0")

                print(f"Endpoint: {name}")
                print(f"  Requests: {requests}, Failures: {failures}, RPS: {rps}")
                print(
                    f"  Response Time (ms) - Min: {min_rt}, Avg: {avg}, Median: {median}, Max: {max_rt}"
                )
                print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run Locust load tests against AIOHTTP servers"
    )
    parser.add_argument(
        "-t", "--time", type=int, default=60, help="Test duration in seconds"
    )
    parser.add_argument(
        "-u", "--users", type=int, default=100, help="Number of users to simulate"
    )
    parser.add_argument(
        "-r", "--spawn-rate", type=int, default=10, help="User spawn rate per second"
    )

    args = parser.parse_args()

    run_locust_test(args.time, args.users, args.spawn_rate)
