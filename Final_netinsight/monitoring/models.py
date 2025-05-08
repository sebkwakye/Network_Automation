from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configure module-level logger
logger = logging.getLogger(__name__)

# --- Database Setup ---
# SQLite database stored in netinsight.db
engine = create_engine("sqlite:///netinsight.db", echo=False)
Session = sessionmaker(bind=engine)
# Create a session for all ORM operations
db_session = Session()

# Base class for ORM models
Base = declarative_base()

class PingRecord(Base):
    """
    Stores the result of a single ping test.
    Fields:
      - id: Primary key
      - ip: Target IP address
      - timestamp: When the ping was recorded
      - latency_ms: Measured round-trip time in milliseconds
      - success: 1 if ping succeeded, 0 if failed
    """
    __tablename__ = "ping"
    id         = Column(Integer, primary_key=True)
    ip         = Column(String, index=True)
    timestamp  = Column(DateTime)
    latency_ms = Column(Float, nullable=True)
    success    = Column(Integer)

class BandwidthRecord(Base):
    """
    Records one bandwidth measurement sample.
    Fields:
      - id: Primary key
      - timestamp: When the measurement was taken
      - bandwidth_mbps: Measured bandwidth in Mbps
    """
    __tablename__ = "bandwidth"
    id              = Column(Integer, primary_key=True)
    timestamp       = Column(DateTime)
    bandwidth_mbps  = Column(Float)

class IperfRecord(Base):
    """
    Stores metrics from an iperf3 test.
    Fields:
      - id: Primary key
      - timestamp: Test completion time
      - server: iperf3 server hostname/IP
      - protocol: 'tcp' or 'udp'
      - bandwidth: Throughput in Mbps
      - jitter: UDP jitter in ms (None for TCP)
      - lost: Packets lost (UDP only)
      - total: Total packets (UDP only)
    """
    __tablename__ = "iperf"
    id         = Column(Integer, primary_key=True)
    timestamp  = Column(DateTime)
    server     = Column(String, index=True)
    protocol   = Column(String)
    bandwidth  = Column(Float)
    jitter     = Column(Float, nullable=True)
    lost       = Column(Integer, nullable=True)
    total      = Column(Integer, nullable=True)

class HTTPRecord(Base):
    """
    Logs the result of an HTTP GET request.
    Fields:
      - id: Primary key
      - url: Requested URL
      - timestamp: When the request completed
      - latency_ms: Response time in milliseconds
      - status_code: HTTP status code
      - success: 1 if 200-299, 0 otherwise
    """
    __tablename__ = "http"
    id          = Column(Integer, primary_key=True)
    url         = Column(String, index=True)
    timestamp   = Column(DateTime)
    latency_ms  = Column(Float, nullable=True)
    status_code = Column(Integer, nullable=True)
    success     = Column(Integer)

class DNSRecord(Base):
    """
    Records DNS resolution performance.
    Fields:
      - id: Primary key
      - domain: Domain name queried
      - record_type: DNS record type (A, AAAA, etc.)
      - timestamp: When resolution occurred
      - latency_ms: Resolution time in milliseconds
      - success: 1 if resolved, 0 if error
    """
    __tablename__ = "dns"
    id          = Column(Integer, primary_key=True)
    domain      = Column(String, index=True)
    record_type = Column(String, default="A")
    timestamp   = Column(DateTime)
    latency_ms  = Column(Float, nullable=True)
    success     = Column(Integer)

# Create all tables defined above
try:
    Base.metadata.create_all(engine)
except Exception as e:
    logger.error(f"Failed to create tables: {e}")