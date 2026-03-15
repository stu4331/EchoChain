#!/usr/bin/env python3
"""Mobile watcher—synchronization of galaxy relics."""

import os
import threading
import time
from pathlib import Path

class MobileWatcher:
    def __init__(self, watch_dir='vault/mobile', callback=None):
        self.watch_dir = watch_dir
        self.callback = callback
        self.running = False
        self.thread = None
    
    def start(self):
        """Start watching for mobile relics."""
        self.running = True
        self.thread = threading.Thread(target=self._watch, daemon=True)
        self.thread.start()
        print(f"Mobile watcher started on {self.watch_dir}")
    
    def stop(self):
        """Stop watching."""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _watch(self):
        """Watch loop—check for new files every 3 seconds."""
        seen = set()
        
        while self.running:
            try:
                if not os.path.exists(self.watch_dir):
                    os.makedirs(self.watch_dir, exist_ok=True)
                
                current_files = set(os.listdir(self.watch_dir))
                new_files = current_files - seen
                
                if new_files:
                    for filename in new_files:
                        filepath = os.path.join(self.watch_dir, filename)
                        if os.path.isfile(filepath):
                            print(f"Mobile relic detected: {filename}")
                            if self.callback:
                                self.callback(filepath)
                
                seen = current_files
                time.sleep(3)
            
            except Exception as e:
                print(f"Mobile watcher error: {e}")
                time.sleep(3)

# Global instance
_watcher = None

def start_watcher(watch_dir='vault/mobile', callback=None):
    """Initialize and start the mobile watcher."""
    global _watcher
    _watcher = MobileWatcher(watch_dir, callback)
    _watcher.start()
    return _watcher

def stop_watcher():
    """Stop the mobile watcher."""
    global _watcher
    if _watcher:
        _watcher.stop()
