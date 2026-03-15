#!/usr/bin/env python3
"""Volatility processes ritual—memory forensics through the vessel."""

import json
import subprocess
import sys

try:
    # Try volatility3 first
    result = subprocess.run(
        ['vol', '-f', '/dev/null', 'windows.pslist'],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        print("Volatility pslist (processes):")
        print(result.stdout)
    else:
        print("No memory image provided for pslist ritual")
        print("Usage: volatility3 -f <memory_file> windows.pslist")
        
except FileNotFoundError:
    print("Volatility tool not inscribed in this vessel")
    print("Install with: pip install volatility3")
except subprocess.TimeoutExpired:
    print("Volatility ritual exceeded time limit")
except Exception as e:
    print(f"Volatility error: {e}")
