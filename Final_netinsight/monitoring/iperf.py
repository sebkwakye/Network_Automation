import logging
import iperf3
from datetime import datetime
from .models import IperfRecord, db_session

# Module-level logger
logger = logging.getLogger(__name__)


def run_iperf(server, port=5201, duration=10, protocol='tcp', bandwidth='1M'):
    """
    Run an iperf3 test to measure network throughput.

    :param server: iperf3 server hostname or IP
    :param port: server port (default 5201)
    :param duration: test duration in seconds (default 10)
    :param protocol: 'tcp' or 'udp'
    :param bandwidth: UDP target bandwidth (e.g. '10M'), ignored for TCP
    :return: IperfRecord saved in the database
    """
    # 1. Configure the client
    client = iperf3.Client()
    client.server_hostname = server
    client.port            = port
    client.duration        = duration
    client.protocol        = protocol.lower()

    # 2. For UDP, set target bandwidth
    if client.protocol == 'udp':
        client.bandwidth = bandwidth

    try:
        # 3. Execute the test
        result = client.run()
    except Exception as e:
        logger.error(f"iperf3 execution failed for {server}: {e}")
        raise RuntimeError(f"iperf3 execution error: {e}")

    # 4. Check for errors in the result
    if result.error:
        logger.error(f"iperf3 reported error: {result.error}")
        raise RuntimeError(f"iperf error: {result.error}")

    # 5. Extract metrics
    throughput = (result.received_Mbps if client.protocol == 'tcp' else result.sent_Mbps)
    jitter     = getattr(result, 'jitter_ms', None)
    lost       = getattr(result, 'lost_packets', None)
    total      = getattr(result, 'packets', None)

    # 6. Save to database
    rec = IperfRecord(
        timestamp = datetime.utcnow(),
        server    = server,
        protocol  = client.protocol,
        bandwidth = throughput,
        jitter    = jitter,
        lost      = lost,
        total     = total
    )
    db_session.add(rec)
    db_session.commit()
    return rec


