import time
import dns.resolver
from datetime import datetime
from .models import DNSRecord, db_session


def test_dns(domain, record_type='A', timeout=5):
    """
    Resolve a DNS record for a given domain and measure resolution time.

    """
    # Initialize resolver and set timeout
    resolver = dns.resolver.Resolver()
    resolver.lifetime = timeout  # max seconds to wait for a response

    # 2. Record the start time in seconds
    start = time.time()

    try:
        # Attempt to resolve the domain
        answers = resolver.resolve(domain, record_type)
        # Calculate latency in milliseconds
        latency = (time.time() - start) * 1000
        ok = 1
    except Exception:
        # On any error, treat as failure
        latency = None
        ok = 0

    # Create and save a DNSRecord to the database
    rec = DNSRecord(
        domain=domain,
        record_type=record_type,
        timestamp=datetime.utcnow(),
        latency_ms=latency,
        success=ok
    )
    db_session.add(rec)
    db_session.commit()

    # Return the saved record
    return rec
