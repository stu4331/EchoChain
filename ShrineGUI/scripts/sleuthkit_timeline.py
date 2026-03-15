#!/usr/bin/env python3
"""SleuthKit timeline ritual—disk forensics through temporal whispers."""

import subprocess
import json

try:
    # Try fls (file list from SleuthKit)
    result = subprocess.run(
        ['fls', '-r', '/'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0 and result.stdout:
        print("SleuthKit file listing (first 20 lines):")
        lines = result.stdout.split('\n')[:20]
        for line in lines:
            print(line)
    else:
        print("SleuthKit timeline ritual requires forensic image")
        print("Usage: fls -r <image_path>")
        print("Or mactime for timeline: mactime -b <bodyfile> <start> <stop>")

except FileNotFoundError:
    print("SleuthKit tools not inscribed—install with:")
    print("  Windows: download from SleuthKit.org")
    print("  Linux: apt-get install sleuthkit")
except Exception as e:
    print(f"SleuthKit error: {e}")
