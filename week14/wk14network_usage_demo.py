'''
Practice Demo: Simulated Bandwidth Logging & Plotting
'''

import csv
import random
import time
from datetime import datetime
import matplotlib.pyplot as plt

CSV_FILE = "network_usage.csv"


def collect_and_store(samples=10, interval=1):
    """
    Simulate network bandwidth collection.
    Every 'interval' seconds, generate a random Mbps value,
    timestamp it, and append to CSV_FILE.
    """
    # Write header
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "bandwidth_mbps"])

    for i in range(samples):
        # Simulate a measurement between 100 and 1000 Mbps
        bw = random.uniform(100, 1000)   # Generates a random floating-point bandwidth between 100 and 1000 Mbps
        ts = datetime.now().isoformat(timespec="seconds")   # current time in ISO format

        # Append to CSV
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([ts, f"{bw:.1f}"])

        print(f"[{ts}] Measured {bw:.1f} Mbps")
        time.sleep(interval)


def plot_usage():
    """
    Read CSV_FILE, extract timestamps and bandwidths,
    and plot a line graph.
    """
    times, values = [], []
    with open(CSV_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(datetime.fromisoformat(row["timestamp"]))
            values.append(float(row["bandwidth_mbps"]))

    plt.figure(figsize=(8, 4))
    plt.plot(times, values, marker='o', linestyle='-')
    plt.title("Simulated Network Bandwidth Over Time")
    plt.xlabel("Time")
    plt.ylabel("Bandwidth (Mbps)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 1) Collect & store simulated data
    collect_and_store(samples=10, interval=1)

    # 2) Plot the results
    plot_usage()
