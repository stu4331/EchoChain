#!/usr/bin/env python3
"""Scapy network analysis plugin—ether whispers decoded."""

import subprocess
import json

class ScapyPlugin:
    @staticmethod
    def pcap_summary(pcap_file=None):
        """Analyze PCAP file for network traffic."""
        try:
            # Use tshark from Wireshark if available
            cmd = ['tshark', '-r', pcap_file or '', '-T', 'fields', '-e', 'ip.src', '-e', 'ip.dst']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[:10]
                return {"success": True, "traffic_summary": lines}
            else:
                return {"error": "No PCAP file or tshark not installed"}
        except FileNotFoundError:
            return {"error": "Wireshark/tshark not found. Use Python Scapy instead."}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def protocol_analysis(pcap_file=None):
        """Analyze protocols in PCAP file."""
        try:
            cmd = ['tshark', '-r', pcap_file or '', '-q', '-z', 'io,phs']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {"protocols": result.stdout if result.returncode == 0 else "Analysis failed"}
        except Exception as e:
            return {"error": str(e)}

if __name__ != '__main__':
    from plugins.registry import register
    register('scapy', ScapyPlugin)
