#!/usr/bin/env python3
"""GPU Hashcat password cracking plugin—lightning through sealed chambers."""

import subprocess
import json
import os

class HashcatPlugin:
    GPU_DEVICE_MAP = {
        'A5000': 'cuda:0',
        'A3000': 'cuda:1',
        'CPU': 'cpu'
    }
    
    @staticmethod
    def crack_hashes(hashfile=None, wordlist=None, hash_type=1000, device='A5000'):
        """
        Invoke GPU-accelerated hashcat on hash file.
        hash_type: 1000 = NTLM, 0 = MD5, 3200 = bcrypt, etc.
        """
        try:
            if not hashfile or not os.path.exists(hashfile):
                return {"error": "Hash file not found", "example": "vault/uploads/hashes.txt"}
            
            if not wordlist or not os.path.exists(wordlist):
                wordlist = '/usr/share/wordlists/rockyou.txt'  # Common default
                if not os.path.exists(wordlist):
                    return {"error": "Wordlist not found", "default_path": wordlist}
            
            device_opt = HashcatPlugin.GPU_DEVICE_MAP.get(device, 'cuda:0')
            
            # Build hashcat command
            cmd = [
                'hashcat',
                '-m', str(hash_type),  # Mode
                '-d', '1,2',  # GPU devices
                '--workload-profile=4',  # Aggressive
                '-O',  # Optimize kernels
                '-w', '4',  # Maximum speed
                hashfile,
                wordlist
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "cracked": result.stdout,
                    "device": device
                }
            else:
                return {
                    "status": "In progress or no matches",
                    "output": result.stdout + result.stderr
                }
        
        except FileNotFoundError:
            return {
                "error": "Hashcat not installed",
                "install": "https://hashcat.net/hashcat/ or apt-get install hashcat"
            }
        except subprocess.TimeoutExpired:
            return {"error": "Hashcat exceeded 5-minute limit"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def list_modes():
        """List all hashcat hash type modes."""
        try:
            result = subprocess.run(
                ['hashcat', '-h'],
                capture_output=True,
                text=True,
                timeout=10
            )
            lines = result.stdout.split('\n')[40:80]  # Approximate mode section
            return {"modes": lines}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def gpu_status(device='A5000'):
        """Check GPU status and capabilities."""
        try:
            result = subprocess.run(
                ['hashcat', '-I'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {"gpu_info": result.stdout}
        except Exception as e:
            return {"error": str(e)}

if __name__ != '__main__':
    from plugins.registry import register
    register('gpu_hashcat', HashcatPlugin)
