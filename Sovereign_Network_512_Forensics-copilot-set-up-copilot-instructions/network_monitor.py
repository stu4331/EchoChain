"""
🌐 HOME NETWORK SECURITY MONITOR
Monitor websites, apps, devices, and detect tampering attempts on your WiFi/LAN network

Features:
- Real-time network traffic capture
- Website/app monitoring  
- Device enumeration
- Threat detection (SQL injection, XSS, suspicious patterns)
- Readable text reports
- Intrusion detection
"""

import threading
import time
import json
import socket
import subprocess
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import ipaddress

try:
    from scapy.all import sniff, IP, TCP, UDP, DNSQR, DNSRR
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

class NetworkMonitor:
    """Monitor home network for security threats and website access"""
    
    def __init__(self, interface=None):
        self.interface = interface
        self.is_monitoring = False
        self.packets_captured = 0
        self.websites_accessed = defaultdict(list)  # {domain: [timestamps]}
        self.devices_seen = {}  # {ip: {mac, hostname, last_seen}}
        self.suspicious_activity = []
        self.threats_detected = []
        self.start_time = None
        
    def get_local_ip(self):
        """Get local machine IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def get_network_interface(self):
        """Get active network interface"""
        if not SCAPY_AVAILABLE:
            return None
            
        try:
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
            # Parse for WiFi or Ethernet adapter
            if 'WiFi' in result.stdout or 'Wireless' in result.stdout:
                return 'WiFi'
            elif 'Ethernet' in result.stdout:
                return 'Ethernet'
        except:
            pass
        return None
    
    def scan_network_devices(self):
        """Scan network for connected devices using ARP"""
        try:
            local_ip = self.get_local_ip()
            network = '.'.join(local_ip.split('.')[:3]) + '.0/24'
            
            # Windows ARP scan
            try:
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if '.' in line and 'bytes' not in line.lower():
                        parts = line.split()
                        if len(parts) >= 2 and self._is_valid_ip(parts[0]):
                            ip = parts[0]
                            mac = parts[1] if len(parts) > 1 else "unknown"
                            self.devices_seen[ip] = {
                                'mac': mac,
                                'first_seen': datetime.now(),
                                'last_seen': datetime.now(),
                                'hostname': self._resolve_hostname(ip)
                            }
            except:
                pass
                
        except Exception as e:
            print(f"Error scanning network: {e}")
    
    def _is_valid_ip(self, ip):
        """Check if string is valid IP"""
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False
    
    def _resolve_hostname(self, ip):
        """Try to resolve IP to hostname"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "unknown"
    
    def analyze_packet(self, packet):
        """Analyze packet for threats and websites"""
        try:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                # Track device
                if self._is_valid_ip(src_ip):
                    if src_ip not in self.devices_seen:
                        self.devices_seen[src_ip] = {
                            'mac': packet[IP].src if hasattr(packet, 'src') else 'unknown',
                            'first_seen': datetime.now(),
                            'last_seen': datetime.now(),
                            'hostname': self._resolve_hostname(src_ip)
                        }
                    else:
                        self.devices_seen[src_ip]['last_seen'] = datetime.now()
            
            # DNS queries (websites being accessed)
            if DNSQR in packet:
                domain = packet[DNSQR].qname.decode('utf-8', errors='ignore').rstrip('.')
                timestamp = datetime.now()
                self.websites_accessed[domain].append(timestamp)
            
            # Check for suspicious patterns in payload
            if TCP in packet or UDP in packet:
                self._check_for_threats(packet)
            
            self.packets_captured += 1
            
        except Exception as e:
            pass
    
    def _check_for_threats(self, packet):
        """Detect SQL injection, XSS, and other attacks"""
        threat_patterns = {
            'SQL_INJECTION': [
                r"(?i)(union.*select|select.*from|drop.*table|insert.*into|delete.*from|update.*set)",
                r"(?i)('.*or.*'|\".*or.*\")",
                r"(?i)(;.*drop|;.*delete|;.*update)"
            ],
            'XSS_ATTACK': [
                r"(?i)(<script|javascript:|onerror=|onload=|alert\()",
                r"(?i)(\<iframe|\<img|src=)",
                r"(?i)(eval\(|exec\()"
            ],
            'COMMAND_INJECTION': [
                r"(?i)(cmd\.exe|powershell|bash|sh\s|\|\s|&&\s|;\s)",
                r"(?i)(\$\(|`)"
            ],
            'DIRECTORY_TRAVERSAL': [
                r"(\.\.\/|\.\.\\|\.\./|\.\.\\)",
                r"(?i)(%2e%2e|..%2f)"
            ]
        }
        
        try:
            # Try to extract payload data
            if TCP in packet:
                load = bytes(packet[TCP].payload)
                payload_str = load.decode('utf-8', errors='ignore').lower()
                
                for threat_type, patterns in threat_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, payload_str):
                            threat = {
                                'timestamp': datetime.now(),
                                'type': threat_type,
                                'source': packet[IP].src if IP in packet else 'unknown',
                                'destination': packet[IP].dst if IP in packet else 'unknown',
                                'pattern': pattern
                            }
                            self.threats_detected.append(threat)
                            break
        except:
            pass
    
    def start_monitoring(self, duration=300):
        """Start monitoring network traffic"""
        if not SCAPY_AVAILABLE:
            return False
        
        self.is_monitoring = True
        self.start_time = datetime.now()
        self.packets_captured = 0
        
        try:
            # First, scan for devices
            self.scan_network_devices()
            
            # Start packet sniffing
            def packet_callback(packet):
                if self.is_monitoring:
                    self.analyze_packet(packet)
            
            # Sniff with timeout
            interface = self.interface or self.get_network_interface()
            if interface:
                sniff(iface=interface, prn=packet_callback, timeout=duration, store=False)
            else:
                sniff(prn=packet_callback, timeout=duration, store=False)
            
            self.is_monitoring = False
            return True
        except PermissionError:
            print("⚠️ Requires administrator/root privileges to capture packets")
            return False
        except Exception as e:
            print(f"Error during monitoring: {e}")
            return False
    
    def start_monitoring_background(self, duration=300):
        """Start monitoring in background thread"""
        thread = threading.Thread(target=self.start_monitoring, args=(duration,))
        thread.daemon = True
        thread.start()
        return thread
    
    def generate_report(self):
        """Generate readable text report"""
        report = []
        report.append("=" * 80)
        report.append("🌐 HOME NETWORK SECURITY MONITOR REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Monitoring Duration: {self._get_duration_string()}")
        report.append(f"Total Packets Captured: {self.packets_captured}")
        report.append("")
        
        # Device Summary
        report.append("-" * 80)
        report.append(f"📱 DEVICES ON NETWORK ({len(self.devices_seen)} total)")
        report.append("-" * 80)
        for ip, info in sorted(self.devices_seen.items()):
            report.append(f"  IP: {ip}")
            report.append(f"     MAC: {info.get('mac', 'unknown')}")
            report.append(f"     Hostname: {info.get('hostname', 'unknown')}")
            report.append(f"     First Seen: {info['first_seen'].strftime('%H:%M:%S')}")
            report.append(f"     Last Seen: {info['last_seen'].strftime('%H:%M:%S')}")
            report.append("")
        
        # Websites Accessed
        report.append("-" * 80)
        report.append(f"🌍 WEBSITES & APPS ACCESSED ({len(self.websites_accessed)} domains)")
        report.append("-" * 80)
        for domain, timestamps in sorted(self.websites_accessed.items(), 
                                        key=lambda x: len(x[1]), reverse=True):
            report.append(f"  {domain}")
            report.append(f"     Accessed: {len(timestamps)} times")
            if timestamps:
                report.append(f"     First: {min(timestamps).strftime('%H:%M:%S')}")
                report.append(f"     Last: {max(timestamps).strftime('%H:%M:%S')}")
            report.append("")
        
        # Threats Detected
        report.append("-" * 80)
        report.append(f"🚨 THREATS DETECTED ({len(self.threats_detected)} total)")
        report.append("-" * 80)
        if self.threats_detected:
            for threat in self.threats_detected:
                report.append(f"  [{threat['timestamp'].strftime('%H:%M:%S')}] {threat['type']}")
                report.append(f"     Source: {threat['source']}")
                report.append(f"     Destination: {threat['destination']}")
                report.append(f"     Pattern: {threat['pattern'][:60]}...")
                report.append("")
        else:
            report.append("  ✅ No threats detected! Your network is secure.")
            report.append("")
        
        # Suspicious Activity
        report.append("-" * 80)
        report.append(f"⚠️ SUSPICIOUS ACTIVITY ({len(self.suspicious_activity)} items)")
        report.append("-" * 80)
        if self.suspicious_activity:
            for activity in self.suspicious_activity:
                report.append(f"  {activity}")
        else:
            report.append("  ✅ No suspicious activity detected.")
        report.append("")
        
        # Summary
        report.append("-" * 80)
        report.append("📊 SECURITY SUMMARY")
        report.append("-" * 80)
        report.append(f"  Safe Websites: {len(self.websites_accessed) - len(self.threats_detected)}")
        report.append(f"  Suspicious Domains: {len(self.threats_detected)}")
        report.append(f"  Active Devices: {len(self.devices_seen)}")
        report.append(f"  Network Status: {'🟢 SECURE' if len(self.threats_detected) == 0 else '🔴 THREATS DETECTED'}")
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_report(self, filename=None):
        """Save report to text file"""
        if filename is None:
            filename = f"network_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        report_path = Path("data/network_reports")
        report_path.mkdir(parents=True, exist_ok=True)
        
        filepath = report_path / filename
        with open(filepath, 'w') as f:
            f.write(self.generate_report())
        
        return str(filepath)
    
    def _get_duration_string(self):
        """Get human-readable duration"""
        if not self.start_time:
            return "Not started"
        duration = datetime.now() - self.start_time
        minutes = duration.total_seconds() // 60
        seconds = int(duration.total_seconds() % 60)
        return f"{int(minutes)}m {seconds}s"
    
    def export_json(self):
        """Export data as JSON"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'packets_captured': self.packets_captured,
            'devices': {ip: {
                'mac': info['mac'],
                'hostname': info['hostname'],
                'first_seen': info['first_seen'].isoformat(),
                'last_seen': info['last_seen'].isoformat()
            } for ip, info in self.devices_seen.items()},
            'websites': {domain: [t.isoformat() for t in timestamps] 
                        for domain, timestamps in self.websites_accessed.items()},
            'threats': [{
                'timestamp': t['timestamp'].isoformat(),
                'type': t['type'],
                'source': t['source'],
                'destination': t['destination']
            } for t in self.threats_detected]
        }
        return json.dumps(data, indent=2)


class NetworkAnalyzer:
    """Analyze network data and generate insights"""
    
    @staticmethod
    def identify_suspicious_domains(websites_accessed, threats_detected):
        """Identify domains with suspicious activity"""
        suspicious = []
        for threat in threats_detected:
            if threat['destination'] not in suspicious:
                suspicious.append(threat['destination'])
        return suspicious
    
    @staticmethod
    def get_top_accessed_domains(websites_accessed, limit=10):
        """Get most frequently accessed domains"""
        return sorted(websites_accessed.items(), 
                     key=lambda x: len(x[1]), 
                     reverse=True)[:limit]
    
    @staticmethod
    def categorize_domain(domain):
        """Categorize domain by type"""
        categories = {
            'social': ['facebook', 'twitter', 'instagram', 'tiktok', 'reddit'],
            'video': ['youtube', 'netflix', 'twitch', 'hulu'],
            'shopping': ['amazon', 'ebay', 'walmart', 'target'],
            'banking': ['bank', 'paypal', 'stripe', 'square'],
            'work': ['slack', 'github', 'gitlab', 'jira', 'outlook'],
            'entertainment': ['gaming', 'steam', 'epic', 'discord']
        }
        
        domain_lower = domain.lower()
        for category, keywords in categories.items():
            if any(keyword in domain_lower for keyword in keywords):
                return category
        return 'other'


if __name__ == "__main__":
    print("🌐 Network Monitor Module Loaded")
    print("Use in GUI: from network_monitor import NetworkMonitor")
