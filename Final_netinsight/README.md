# NetInsight Network Monitoring

## Overview

NetInsight is a Python-based network monitoring dashboard that provides real‑time insights into:

**Ping latency** to arbitrary hosts

**Bandwidth** sampling

**HTTP** response timing

**DNS** resolution timing

**GeoIP** lookups

**BGP** prefix counts

**iPerf3** throughput tests

Built with Flask, Chart.js, SQLAlchemy (SQLite), and Bootstrap.

## Installation & Setup
### 1. Clone repository
git clone 
https://github.com/sebkwakye/Network_Automation/Final_netinsight.git
https://github.com/sebkwakye/Network_Automation/tree/891940b0f0836193cad5354592b12b060ad6c735/Final_netinsight


cd netinsight

### 2. Create a virtual environment
python3 -m venv venv

source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Initialize the database (SQLite)
python - << 'EOF'
from monitoring.models import Base, engine
Base.metadata.create_all(engine)
EOF

## Running the Application
### Activate venv first if not already active
export FLASK_APP=flask_app.app:create_app

flask run --reload
### Dashboard available at http://localhost:5000/

## Usage & Parameters

Each section has its own controls:

**Ping Test**

Enter an IPv4/IPv6 address or hostname

Click Run Ping

Shows latest latency graph and status

**Bandwidth Test**

Click Run Bandwidth to collect 3 samples

Graph updates in real time

**HTTP Test**

Enter a URL (e.g., https://example.com)

Click Run HTTP

Graph historical response times

**DNS Test**

Enter a domain (e.g., www.google.com)

Click Run DNS

Graph historical resolution times

**GeoIP Lookup**

Enter an IP address

Click Lookup GeoIP

Shows JSON location data

**BGP Prefix Count**

Enter an ASN (e.g., 15169)

Click Get BGP

Displays IPv4/IPv6 prefix counts

**iPerf3 Test**

Provide an iPerf3 server hostname or IP

Click Run iPerf

Reports throughput and updates bar chart

