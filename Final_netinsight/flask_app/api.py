from flask import Blueprint, request, jsonify
import logging

from monitoring.ping import monitor_ips, PingRecord
from monitoring.bandwidth import simulate_samples
from monitoring.iperf import run_iperf, IperfRecord
from monitoring.http import test_http, HTTPRecord
from monitoring.dns import test_dns, DNSRecord
from monitoring.external import geoip_lookup, bgp_prefix_count
from monitoring.models import db_session

# Blueprint for API routes
api = Blueprint('api', __name__, url_prefix='/api')
# Module-level logger
g_logger = logging.getLogger(__name__)

# --- Ping Endpoints ---
@api.route('/ping/run', methods=['POST'])
def api_ping_run():
    """
    Trigger ping tests for a list of IPs.
    Expects JSON: {"ips": [...], "count": int, "interval": int}
    """
    payload = request.json or {}
    ips      = payload.get('ips', [])
    count    = int(payload.get('count', 8))
    interval = int(payload.get('interval', 15))
    if not ips:
        return jsonify({'error': 'No IPs provided'}), 400

    monitor_ips(ips, count, interval)
    return jsonify({'status': 'started', 'ips': ips}), 202

@api.route('/ping/results', methods=['GET'])
def api_ping_results():
    """
    Return all stored ping records.
    """
    records = db_session.query(PingRecord).all()
    return jsonify([
        {
            'ip':      r.ip,
            'time':    r.timestamp.isoformat(),
            'latency': r.latency_ms,
            'success': bool(r.success)
        } for r in records
    ])

# --- Bandwidth Endpoints ---
@api.route('/bw/run', methods=['GET'])
def api_bw_run():
    """
    Run n bandwidth tests. Query params: n (int), interval (int).
    """
    n        = int(request.args.get('n', 3))
    interval = int(request.args.get('interval', 60))
    samples  = simulate_samples(n, interval)
    return jsonify([
        {
            'time': r.timestamp.isoformat(),
            'bw':   r.bandwidth_mbps
        } for r in samples
    ])

# --- iPerf Endpoints ---
@api.route('/iperf/run', methods=['POST'])
def api_iperf_run():
    """
    Trigger an iperf3 test.
    JSON body: {"server":"host", "protocol":"tcp|udp", "duration":int, "bandwidth":"10M"}
    """
    payload  = request.json or {}
    server   = payload.get('server')
    if not server:
        return jsonify({'error': 'No server provided'}), 400
    protocol = payload.get('protocol', 'tcp')
    duration = int(payload.get('duration', 10))
    bw       = payload.get('bandwidth', '1M')
    try:
        rec = run_iperf(server, duration=duration, protocol=protocol, bandwidth=bw)
    except Exception as e:
        g_logger.error(f"iPerf test failed: {e}")
        return jsonify({'error': str(e)}), 500
    return jsonify({
        'timestamp': rec.timestamp.isoformat(),
        'server':    rec.server,
        'protocol':  rec.protocol,
        'bandwidth': rec.bandwidth,
        'jitter':    rec.jitter,
        'lost':      rec.lost,
        'total':     rec.total
    }), 201

@api.route('/iperf/results', methods=['GET'])
def api_iperf_results():
    """Return stored iperf3 test results."""
    rows = db_session.query(IperfRecord).all()
    return jsonify([
        {
            'time':      r.timestamp.isoformat(),
            'server':    r.server,
            'protocol':  r.protocol,
            'bandwidth': r.bandwidth,
            'jitter':    r.jitter,
            'lost':      r.lost,
            'total':     r.total
        } for r in rows
    ])

# --- HTTP Endpoints ---
@api.route('/http/run', methods=['POST'])
def api_http_run():
    """
    Trigger an HTTP GET test.
    JSON body: {"url":"https://..."}
    """
    payload = request.json or {}
    url     = payload.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    rec = test_http(url)
    return jsonify({
        'time': rec.timestamp.isoformat(),
        'url':  rec.url,
        'latency': rec.latency_ms,
        'status':  rec.status_code,
        'success': bool(rec.success)
    }), 201

@api.route('/http/results', methods=['GET'])
def api_http_results():
    """Return stored HTTP test results."""
    rows = db_session.query(HTTPRecord).all()
    return jsonify([
        {
            'time':   r.timestamp.isoformat(),
            'url':    r.url,
            'latency':r.latency_ms,
            'status': r.status_code,
            'success':bool(r.success)
        } for r in rows
    ])

# --- DNS Endpoints ---
@api.route('/dns/run', methods=['POST'])
def api_dns_run():
    """
    Trigger a DNS resolution test.
    JSON body: {"domain":"...", "type":"A"}
    """
    payload = request.json or {}
    domain  = payload.get('domain')
    if not domain:
        return jsonify({'error': 'No domain provided'}), 400
    rtype = payload.get('type', 'A')
    rec = test_dns(domain, record_type=rtype)
    return jsonify({
        'time':    rec.timestamp.isoformat(),
        'domain':  rec.domain,
        'type':    rec.record_type,
        'latency': rec.latency_ms,
        'success': bool(rec.success)
    }), 201

@api.route('/dns/results', methods=['GET'])
def api_dns_results():
    """Return stored DNS test results."""
    rows = db_session.query(DNSRecord).all()
    return jsonify([
        {
            'time':    r.timestamp.isoformat(),
            'domain':  r.domain,
            'type':    r.record_type,
            'latency': r.latency_ms,
            'success':bool(r.success)
        } for r in rows
    ])

# --- External APIs ---
@api.route('/geoip/<ip>', methods=['GET'])
def api_geoip(ip):
    """Return geolocation data for an IP."""
    data = geoip_lookup(ip)
    return jsonify(data)

@api.route('/bgp/<int:asn>', methods=['GET'])
def api_bgp(asn):
    """Return prefix counts for an ASN."""
    data = bgp_prefix_count(asn)
    return jsonify(data)

