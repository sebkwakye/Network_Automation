'''
Task: You are tasked with developing a network monitoring tool that will monitor the responsiveness of at least three separate IP addresses.
The tool should collect information such as latency and packet loss and store this data into a database. Additionally, you should
implement functionality to analyze the collected data and provide insights such as which Google DNS server responds faster from your
 current location and network routes.
'''

#!/usr/bin/env python3
"""
network_monitor.py

A simple tool to ping a list of IP addresses, record latency and packet loss
into a SQLite database, analyze the results, and (optionally) visualize them.
"""

import argparse
import platform
import sqlite3
import subprocess
import time
from datetime import datetime

# --- Configuration Constants ---
DB_FILE = "monitoring.db"          # SQLite database file
PING_COUNT = 8                     # Number of pings per IP
PING_INTERVAL = 15                 # Seconds between each round of pings

# --- Database Schema ---
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ping_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    latency_ms REAL,
    success INTEGER NOT NULL
);
"""

def setup_database():
    """Create the SQLite database and the ping_data table if needed."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()


def ping_once(ip, timeout_ms=1000):
    """
    Ping the given IP once.
    Returns (success: bool, latency_ms: float or None).
    """
    # Select the right flag for count (-c on Linux/Mac, -n on Windows)
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    # Build the ping command
    cmd = ["ping", count_flag, "1", "-W", str(timeout_ms), ip]

    try:
        # Run the ping command
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

        if result.returncode != 0:
            # Non-zero return code means ping failed
            return False, None

        # Look for something like "time=23.4 ms" in the output
        for token in output.split():
            if token.startswith("time"):
                # token could be "time=23.4" or "time<1"
                num_part = token.replace("time=", "").replace("ms", "").replace("<", "")
                return True, float(num_part)
        # fallback if parsing fails
        return True, 0.0

    except Exception:
        # If something went wrong calling ping at all
        return False, None


def record_ping(ip, success, latency):
    """
    Insert one ping result into the database.
    success: 1 for up, 0 for down.
    latency: float in ms or None.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO ping_data (ip, timestamp, latency_ms, success) VALUES (?, ?, ?, ?)",
        (ip, timestamp, latency, 1 if success else 0)
    )
    conn.commit()
    conn.close()


def monitor_ips(ips, count=PING_COUNT, interval=PING_INTERVAL):
    """
    Ping each IP `count` times, waiting `interval` seconds between rounds.
    All results are saved in the database.
    """
    print(f"Monitoring {len(ips)} IPs, {count} pings each, {interval}s apart.")
    setup_database()

    for round_num in range(1, count + 1):
        print(f"\n--- Round {round_num}/{count} at {datetime.now().strftime('%H:%M:%S')} ---")
        for ip in ips:
            success, latency = ping_once(ip)
            record_ping(ip, success, latency)
            status = "✔" if success else "✘"
            latency_str = f"{latency:.1f} ms" if latency is not None else "timeout"
            print(f"{status} {ip:12} → {latency_str}")
        if round_num < count:
            time.sleep(interval)

    print("\nDone monitoring.")


def analyze_results(ips):
    """
    Read the database and compute, for each IP:
      - total probes
      - success count
      - packet loss %
      - average latency
    Then print the results, and identify the faster Google DNS.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    stats = {}
    for ip in ips:
        cursor.execute(
            "SELECT COUNT(*), SUM(success), AVG(latency_ms) FROM ping_data WHERE ip = ?",
            (ip,)
        )
        total, success_sum, avg_latency = cursor.fetchone()
        total = total or 0
        success_sum = success_sum or 0
        packet_loss = 100 * (1 - success_sum/total) if total else None

        stats[ip] = {
            "total": total,
            "successes": success_sum,
            "avg_latency": avg_latency,
            "packet_loss": packet_loss
        }

    conn.close()

    print("\n=== Analysis ===")
    for ip, s in stats.items():
        print(f"{ip}:")
        print(f"  Probes: {s['total']}, Successes: {s['successes']}")
        if s['packet_loss'] is not None:
            print(f"  Packet loss: {s['packet_loss']:.1f}%")
        if s['avg_latency'] is not None:
            print(f"  Avg latency: {s['avg_latency']:.1f} ms")
        print()

    # Compare Google DNS servers
    googles = {ip: s for ip, s in stats.items() if ip in ("8.8.8.8", "8.8.4.4")}
    if googles:
        fastest = min(
            (ip for ip in googles if googles[ip]["avg_latency"] is not None),
            key=lambda ip: googles[ip]["avg_latency"],
            default=None
        )
        if fastest:
            print(f"Fastest Google DNS: {fastest} ({googles[fastest]['avg_latency']:.1f} ms)")


def main():
    # 1) Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Ping a list of IPs, log results, and analyze them."
    )
    parser.add_argument(
        "--ips", nargs="+", required=True,
        help="IP addresses to monitor (include 8.8.8.8 and 8.8.4.4)."
    )
    args = parser.parse_args()

    # 2) Run monitoring
    monitor_ips(args.ips)

    # 3) Analyze the stored data
    analyze_results(args.ips)


if __name__ == "__main__":
    main()
