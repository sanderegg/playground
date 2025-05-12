#!/usr/bin/env python3
"""
Script to find the maximum sustainable RPS for each server implementation.
This script runs multiple tests with increasing load until the server starts to fail.
"""

import argparse
import csv
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple


def run_single_test(
    users: int,
    spawn_rate: int,
    duration: int,
    results_dir: Path,
    prefix: str,
) -> Dict:
    """Run a single Locust test with specified parameters.

    Args:
        users: Number of users to simulate
        spawn_rate: Rate at which to spawn users per second
        duration: Duration of the test in seconds
        results_dir: Directory to save results
        prefix: Prefix for result files

    Returns:
        Dictionary with test results
    """
    print(
        f"Running test with {users} users at spawn rate {spawn_rate}/s for {duration}s"
    )

    cmd = [
        "locust",
        "--headless",
        "--users",
        str(users),
        "--spawn-rate",
        str(spawn_rate),
        "--run-time",
        f"{duration}s",
        "--csv",
        str(results_dir / f"{prefix}"),
        "--only-summary",
        "-f",
        str(Path(__file__).parent / "locustfile.py"),
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

    # Parse results
    stats_file = results_dir / f"{prefix}_stats.csv"
    if not stats_file.exists():
        return {"error": "No results file found"}

    with open(stats_file, "r") as f:
        reader = csv.DictReader(f)
        results = list(reader)

    return {
        row["Name"]: float(row["Requests/s"])
        for row in results
        if "Aggregated" not in row["Name"]
    }


def find_max_rps_binary_search(
    server_name: str,
    initial_users: int,
    max_users: int,
    duration: int,
    results_dir: Path,
    failure_threshold: float = 1.0,
) -> Tuple[int, float]:
    """Find the maximum RPS using binary search approach.

    Args:
        server_name: Name of the server (for result identification)
        initial_users: Starting number of users
        max_users: Maximum number of users to try
        duration: Duration of each test in seconds
        results_dir: Directory to save results
        failure_threshold: Threshold for failure percentage to consider a test failed

    Returns:
        Tuple of (max users, max RPS)
    """
    low = initial_users
    high = max_users
    best_users = 0
    best_rps = 0

    results = []

    # Initial test with low users
    prefix = f"{server_name}_initial"
    initial_result = run_single_test(low, low, duration, results_dir, prefix)
    results.append((low, initial_result))

    if not initial_result or "error" in initial_result:
        print(f"Error in initial test for {server_name}")
        return 0, 0

    # Get the specific result for this server
    server_key = [key for key in initial_result.keys() if server_name in key]
    if not server_key:
        print(f"Could not find results for {server_name}")
        return 0, 0

    server_key = server_key[0]
    best_rps = initial_result[server_key]
    best_users = low

    print(f"Initial test: {low} users achieved {best_rps:.2f} RPS")

    # Binary search for max RPS
    while low <= high:
        mid = (low + high) // 2

        if mid == best_users:
            # We've converged
            break

        prefix = f"{server_name}_{mid}"
        result = run_single_test(mid, min(mid, 100), duration, results_dir, prefix)
        results.append((mid, result))

        if not result or "error" in result or server_key not in result:
            # Test failed completely
            high = mid - 1
            continue

        current_rps = result[server_key]

        # Check for failures
        failure_file = results_dir / f"{prefix}_failures.csv"
        failure_rate = 0
        if failure_file.exists() and os.path.getsize(failure_file) > 0:
            with open(failure_file, "r") as f:
                failures = list(csv.DictReader(f))
                if failures:
                    # Get the total number of requests from the stats file
                    stats_file = results_dir / f"{prefix}_stats.csv"
                    if stats_file.exists():
                        with open(stats_file, "r") as sf:
                            stats = list(csv.DictReader(sf))
                            total_requests = sum(
                                int(float(row["Request Count"]))
                                for row in stats
                                if server_key == row["Name"]
                            )
                            total_failures = sum(
                                int(row["Occurrences"]) for row in failures
                            )
                            if total_requests > 0:
                                failure_rate = (total_failures / total_requests) * 100

        print(
            f"Users: {mid}, RPS: {current_rps:.2f}, Failure rate: {failure_rate:.2f}%"
        )

        if failure_rate > failure_threshold:
            # Too many failures, go lower
            high = mid - 1
        else:
            # Success, record and try higher
            if current_rps > best_rps:
                best_rps = current_rps
                best_users = mid
            low = mid + 1

    # Save all results to JSON for analysis
    with open(results_dir / f"{server_name}_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return best_users, best_rps


def find_max_rps_for_all_servers() -> None:
    """Find and report the maximum RPS for all three server implementations."""
    parser = argparse.ArgumentParser(
        description="Find maximum sustainable RPS for AIOHTTP server implementations"
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=30,
        help="Duration of each test in seconds",
    )
    parser.add_argument(
        "-i", "--initial", type=int, default=50, help="Initial number of users"
    )
    parser.add_argument(
        "-m", "--max", type=int, default=1000, help="Maximum number of users to try"
    )
    parser.add_argument(
        "-f",
        "--failure-threshold",
        type=float,
        default=1.0,
        help="Failure percentage threshold (0-100) to consider a test failed",
    )

    args = parser.parse_args()

    # Create results directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / "results" / f"max_rps_{timestamp}"
    os.makedirs(results_dir, exist_ok=True)

    print(
        f"Finding maximum RPS for all servers. Results will be saved to {results_dir}"
    )
    print(
        f"Test parameters: duration={args.duration}s, initial={args.initial} users, max={args.max} users"
    )
    print(f"Failure threshold: {args.failure_threshold}%")

    servers = [
        ("Simple", "Simple Server"),
        ("Gunicorn", "Gunicorn Server"),
        ("Gunicorn+uvloop", "Gunicorn+uvloop Server"),
    ]

    results = []

    for server_id, server_name in servers:
        print(f"\n{'-'*60}")
        print(f"Testing {server_name}")
        print(f"{'-'*60}")

        max_users, max_rps = find_max_rps_binary_search(
            server_id,
            args.initial,
            args.max,
            args.duration,
            results_dir,
            args.failure_threshold,
        )

        results.append((server_name, max_users, max_rps))

        # Let the system cool down between tests
        print("Cooling down for 10 seconds before next test...")
        time.sleep(10)

    # Print summary
    print(f"\n{'-'*60}")
    print("SUMMARY OF RESULTS")
    print(f"{'-'*60}")
    print(f"{'Server Type':<25} {'Max Users':<10} {'Max RPS':<10}")
    print(f"{'-'*60}")
    for server_name, max_users, max_rps in results:
        print(f"{server_name:<25} {max_users:<10} {max_rps:<10.2f}")

    # Save summary to file
    with open(results_dir / "summary.txt", "w") as f:
        f.write("MAXIMUM RPS TEST RESULTS\n")
        f.write(f"Test Date: {timestamp}\n")
        f.write(
            f"Test Parameters: duration={args.duration}s, initial={args.initial} users, max={args.max} users\n"
        )
        f.write(f"Failure Threshold: {args.failure_threshold}%\n\n")

        f.write(f"{'Server Type':<25} {'Max Users':<10} {'Max RPS':<10}\n")
        f.write(f"{'-'*50}\n")
        for server_name, max_users, max_rps in results:
            f.write(f"{server_name:<25} {max_users:<10} {max_rps:<10.2f}\n")

    print(f"\nTest completed. Results saved to {results_dir}/summary.txt")


if __name__ == "__main__":
    find_max_rps_for_all_servers()
