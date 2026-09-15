# Computer Networking Lab Portfolio

![Python](https://img.shields.io/badge/Python-network_programming-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TCP/IP](https://img.shields.io/badge/Protocols-DNS%20%7C%20WHOIS%20%7C%20HTTP%20%7C%20TCP-0A7EA4?style=flat-square)
![Scapy](https://img.shields.io/badge/Packet_tools-Scapy-E95420?style=flat-square)
![Flask](https://img.shields.io/badge/Web_layer-Flask-000?style=flat-square&logo=flask)

A progressive collection of Python networking labs that moves from public web APIs into the mechanics beneath them: name resolution, WHOIS, raw HTTP, TCP flags and sequence numbers, packet crafting, traceroute, and autonomous-system lookup.

This repository is best read as an engineering progression. Each lab removes another abstraction layer until the application is constructing and inspecting packets directly.

## Project progression

| Lab | Focus | What it demonstrates |
|---|---|---|
| `lab2.py` | WHOIS → geocoding → weather | Combines DNS, command-line tools, JSON APIs, address normalization, and temperature plotting |
| `lab3.py` | Flask service and caching | Exposes address, forecast, and network-range lookups as routes with in-memory result caches |
| `lab4.py` | Raw HTTP client | Opens a TCP socket, writes an HTTP/1.1 request, receives the response, and prints or saves the result |
| `lab6.py` | Manual TCP + HTTP with Scapy | Builds SYN/ACK/PSH packet exchanges and reasons about sequence and acknowledgment numbers |
| `lab7.py` | Traceroute and AS discovery | Varies packet TTL, records intermediate hops, and queries Team Cymru WHOIS for AS numbers |

Earlier and experimental variants are retained to show iteration, troubleshooting, and platform-specific exploration.

## 1. Domain intelligence and weather pipeline

`lab2.py` accepts a hostname or IP address and connects several systems into one pipeline:

```text
domain / IP
    ↓
DNS resolution + WHOIS
    ↓
registrant address parsing
    ↓
U.S. Census geocoding
    ↓
weather.gov grid + hourly forecast
    ↓
terminal output / Matplotlib chart
```

The interesting work is not only making requests; it is translating one system's output into the next system's input and handling inconsistent address formats along the way.

Example:

```bash
python3 lab2.py example.com
```

## 2. Turning the pipeline into a service

`lab3.py` wraps the lookup logic in Flask and adds simple in-memory caches for addresses, weather results, and network ranges. It exposes routes including:

```text
/address/<domain>
/weather/<domain>
/range/<domain>
/upper/<text>
/callwhois/<domain>
```

Run it with:

```bash
python3 lab3.py
```

Then request a route such as `http://127.0.0.1:5000/address/example.com`.

## 3. HTTP without a browser or client library

`lab4.py` uses Python's socket API to connect to a host, compose the HTTP request text, read the response in chunks, separate headers from the response body, and either print or save the result.

```bash
python3 lab4.py -p 80 example.com/
python3 lab4.py -f 80 example.com/
```

This lab makes the boundary between TCP transport and HTTP application data visible.

## 4. Packet-level TCP

`lab6.py` goes below connected sockets and uses Scapy to assemble IP/TCP packets. It initiates a handshake, acknowledges the server's response, sends an HTTP request using PSH/ACK, and processes the returning packet data.

```bash
sudo python3 lab6.py example.com
```

Raw packet operations commonly require elevated privileges and may be affected by the host operating system's TCP stack or firewall.

## 5. Route and autonomous-system discovery

`lab7.py` implements a TCP-oriented traceroute by increasing the IP TTL one hop at a time. ICMP time-exceeded responses reveal the route; a SYN/ACK indicates the target has been reached. Each responding hop is also checked against Team Cymru's WHOIS service to collect unique AS numbers.

```bash
sudo python3 lab7.py example.com 20
```

The result connects packet behavior to the real administrative structure of the Internet.

## Setup

Python 3 is required. The labs collectively use Flask, Requests, Matplotlib, NumPy, and Scapy, plus command-line `whois`/`nslookup` support.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install flask requests matplotlib numpy scapy
```

Some endpoints target U.S. government services and depend on live network access. WHOIS output differs between registries, so the parsing labs are also useful examples of working with imperfect external data.

## Repository map

```text
.
├── lab2.py                            # CLI lookup, geocoding, forecast, graph
├── lab3.py                            # Flask API and caches
├── lab4.py                            # Socket-based HTTP client
├── lab6.py                            # Scapy TCP handshake and HTTP request
├── lab7.py                            # Traceroute and AS-number lookup
├── lab2OLD.py / lab3Old*.py           # Earlier iterations and experiments
├── lab3forecast.py / lab3range.py     # Focused feature branches
├── output.txt                         # Captured HTTP output
└── test.sh                            # Command-line test helper
```

## Skills demonstrated

TCP/IP fundamentals, protocol debugging, sockets, packet construction, TTL/ICMP behavior, HTTP framing, DNS and WHOIS, API integration, JSON parsing, caching, Flask routing, CLI design, and iterative development.
