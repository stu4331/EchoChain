#!/usr/bin/env python3
"""SleuthKit disk analysis plugin—timeline reconstructed."""

import subprocess
import json

class SleuthtoolPlugin:
    @staticmethod
    def timeline(image_path=None):
        """Generate disk timeline from forensic image."""
        try:
            cmd = ['fls', '-r', image_path or '/']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {"success": True, "timeline": result.stdout[:1000]}
            else:
                return {"error": "No forensic image provided"}
        except FileNotFoundError:
            return {"error": "SleuthKit tools not installed"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def inode_analysis(image_path=None, inode=None):
        """Analyze specific inode from image."""
        try:
            cmd = ['istat', image_path or '/', inode or '0']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {"inode_info": result.stdout if result.returncode == 0 else "Failed"}
        except Exception as e:
            return {"error": str(e)}

if __name__ != '__main__':
    from plugins.registry import register
    register('sleuthkit', SleuthtoolPlugin)
