import time
from datetime import datetime
from speedtest import Speedtest
from .models import BandwidthRecord, db_session


def collect_real_bandwidth():
    """
    Perform a real speedtest download measurement and store it.

    """
    st = Speedtest()
    st.get_best_server()  # Select nearest/fastest server
    download_bps = st.download()  # Download speed in bits/sec
    download_mbps = download_bps / 1e6  # Convert to Mbps

    # Create and save the record
    rec = BandwidthRecord(
        timestamp=datetime.utcnow(),
        bandwidth_mbps=download_mbps
    )
    db_session.add(rec)
    db_session.commit()
    return rec


def simulate_samples(n=3, interval=60):
    """
    Run n real speedtests, waiting interval seconds between each.
    Note: Each speedtest can take 10–20 seconds.
    """
    results = []
    for i in range(n):
        rec = collect_real_bandwidth()
        results.append(rec)
        if i < n - 1:
            time.sleep(interval)
    return results
