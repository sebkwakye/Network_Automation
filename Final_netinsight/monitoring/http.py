import time
import logging
import requests
from datetime import datetime
from .models import HTTPRecord, db_session

# Module-level logger
logger = logging.getLogger(__name__)


def test_http(url, timeout=5):
    """
    Perform an HTTP GET on `url`, measure latency in ms, and record status.

    :param url: target URL to test
    :param timeout: request timeout in seconds
    :return: HTTPRecord instance saved to the database
    """
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout)
        latency = (time.time() - start) * 1000  # convert to milliseconds
        status = response.status_code
        success = 1 if response.ok else 0
    except requests.exceptions.RequestException as e:
        # Log network errors, timeouts, invalid URLs, etc.
        logger.error(f"HTTP test error for {url}: {e}")
        latency = None
        status = None
        success = 0

    # Create and save record
    rec = HTTPRecord(
        url=url,
        timestamp=datetime.utcnow(),
        latency_ms=latency,
        status_code=status,
        success=success
    )
    db_session.add(rec)
    db_session.commit()
    return rec
