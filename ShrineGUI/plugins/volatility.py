#!/usr/bin/env python3
"""Volatility memory analysis plugin—volatile landscapes traversed."""

import subprocess
import json

class VolatilityPlugin:
    @staticmethod
    def pslist(memory_file=None, gpu='A5000'):
        """List processes from memory dump."""
        try:
            cmd = ['vol', '-f', memory_file or '/dev/null', 'windows.pslist']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {"success": True, "processes": result.stdout}
            else:
                return {"error": "No valid memory image or volatility3 not installed"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def netscan(memory_file=None):
        """Scan network connections from memory."""
        try:
            cmd = ['vol', '-f', memory_file or '/dev/null', 'windows.netscan']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {"success": True, "connections": result.stdout}
            else:
                return {"error": "Network scan failed"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def handles(memory_file=None):
        """Extract file handles from memory."""
        try:
            cmd = ['vol', '-f', memory_file or '/dev/null', 'windows.handles']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            return {"handles": result.stdout if result.returncode == 0 else "Failed"}
        except Exception as e:
            return {"error": str(e)}

if __name__ != '__main__':
    from plugins.registry import register
    register('volatility', VolatilityPlugin)
