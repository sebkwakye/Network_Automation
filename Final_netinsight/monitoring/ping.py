import logging
import platform
import subprocess
import time
from datetime import datetime
from .models import PingRecord, db_session

# Module-level logger
t_logger = logging.getLogger(__name__)


def ping_once(ip, timeout_ms=1000):
    """
    Send a single ping to the given IP and measure latency.

    :param ip: target IP address or hostname
    :param timeout_ms: timeout in milliseconds for the ping
    :return: (success: bool, latency_ms: float or None)
    """
    # Choose correct ping flag for count depending on OS
    count_flag = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = [
        'ping', count_flag, '1',
        '-W', str(timeout_ms),  # timeout flag (seconds on Unix)
        ip
    ]
    try:
        # Run the ping command, capture output, apply a subprocess timeout
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=(timeout_ms / 1000) + 1
        )
        # Non-zero return code indicates failure
        if res.returncode != 0:
            return False, None

        # Parse output for 'time=' token
        for tok in res.stdout.split():
            if tok.startswith('time'):
                # token like 'time=23.4' or 'time<1'
                num = tok.replace('time=', '').replace('ms', '').replace('<', '')
                try:
                    return True, float(num)
                except ValueError:
                    return True, 0.0
        # If 'time' not found, assume success but unknown latency
        return True, 0.0

    except subprocess.TimeoutExpired:
        t_logger.warning(f"Ping to {ip} timed out after {timeout_ms}ms")
        return False, None
    except Exception as e:
        t_logger.error(f"Error executing ping to {ip}: {e}")
        return False, None


def record_ping(ip, success, latency):
    """
    Save a ping result into the database.

    :param ip: the IP that was pinged
    :param success: 1 if ping succeeded, 0 otherwise
    :param latency: measured latency in ms or None
    """
    rec = PingRecord(
        ip=ip,
        timestamp=datetime.utcnow(),
        latency_ms=latency,
        success=1 if success else 0
    )
    db_session.add(rec)
    db_session.commit()


def monitor_ips(ips, count=8, interval=15):
    """
    Ping a list of IPs multiple times, recording each result.

    :param ips: list of IP addresses or hostnames to monitor
    :param count: number of ping iterations per IP
    :param interval: seconds to wait between iterations
    """
    for i in range(count):
        for ip in ips:
            ok, lat = ping_once(ip)
            record_ping(ip, ok, lat)
        # Wait before next round, but skip sleep after last
        if i < count - 1:
            time.sleep(interval)
