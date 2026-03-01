# 🌐 Network & Web Tools Collection

**Author:** Kenton Bell  

A collection of small networking and web-focused Python projects demonstrating socket programming, API usage, packet crafting, and lightweight web services.

---

## 📚 Index

1. WHOIS → Geocoding → Weather CLI Tool  
2. Flask WHOIS & Weather Web App (with Caching)  
3. Raw Socket HTTP Client  
4. Manual TCP Handshake + HTTP (Scapy)  
5. Traceroute with AS Lookup (Scapy)  

---

## 📖 About

This repository contains several independent mini-projects focused on:

- DNS resolution and WHOIS lookups  
- Address parsing and geocoding  
- REST API interaction (`weather.gov`, Census geocoder)  
- Raw TCP socket programming  
- Manual packet crafting with Scapy  
- Traceroute implementation with AS number extraction  
- Basic Flask web service development  

Each project explores lower-level networking concepts and how web systems operate under the hood.

---

## 🛠 Usage

### 1️⃣ CLI Weather & WHOIS Tool
- Accepts a domain or IP
- Performs WHOIS lookup
- Extracts address
- Geocodes via Census API
- Fetches weather from weather.gov
- Plots hourly temperatures using Matplotlib  
