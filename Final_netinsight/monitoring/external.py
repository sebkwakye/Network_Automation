import logging
import requests

# Configure a module-level logger
logger = logging.getLogger(__name__)


def geoip_lookup(ip):
    """
    Fetch geolocation information for an IP via ipinfo.io.

    :param ip: IP address to look up
    :return: dict of location data or empty dict on error
    """
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"GeoIP lookup failed for {ip}: {e}")
    except ValueError as e:
        logger.error(f"Invalid JSON in GeoIP response for {ip}: {e}")
    return {}


def bgp_prefix_count(asn):
    """
    Retrieve counts of IPv4 and IPv6 prefixes for a given ASN via BGPView.

    :param asn: Autonomous System Number (integer)
    :return: {'ipv4': int, 'ipv6': int} or {'ipv4':0,'ipv6':0} on error
    """
    url = f"https://api.bgpview.io/asn/{asn}/prefixes"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json().get('data', {})
        return {
            'ipv4': len(data.get('ipv4_prefixes', [])),
            'ipv6': len(data.get('ipv6_prefixes', []))
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"BGP prefix count failed for ASN {asn}: {e}")
    except ValueError as e:
        logger.error(f"Invalid JSON in BGPView response for ASN {asn}: {e}")
    return {'ipv4': 0, 'ipv6': 0}
