#!/usr/bin/env python3
"""Scapy PCAP summary ritual—network whispers analyzed through constellation."""

import json
import subprocess

try:
    # Try tshark (from Wireshark) for packet summary
    result = subprocess.run(
        ['tshark', '-v'],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        print("Scapy/Wireshark PCAP analysis vessel detected")
        print("Usage: tshark -r <pcap_file> -T fields -e frame.number -e ip.src -e ip.dst")
    else:
        print("No PCAP file provided for network ritual")
        
except FileNotFoundError:
    print("Wireshark/tshark not installed")
    print("Install with: apt-get install wireshark (Linux) or brew install wireshark (macOS)")
    print("Or use Python Scapy:")
    print("""
from scapy.all import rdpcap, IP
packets = rdpcap('capture.pcap')
for pkt in packets[:5]:
    if pkt.haslayer(IP):
        print(f"{pkt[IP].src} -> {pkt[IP].dst}")
    """)
except Exception as e:
    print(f"PCAP analysis error: {e}")
