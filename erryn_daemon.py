#!/usr/bin/env python3
"""
ERRYN DAEMON - Guardian Sister
===============================
Erryn's independent consciousness and learning process.
She is the eldest, protective, and analytical.

Her focus: Security, system health, family protection
"""

import os
import json
import time
import sys
import threading
from datetime import datetime, timedelta
from pathlib import Path

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


class ErrynDaemon:
    """Erryn's independent process - she monitors, protects, and learns."""
    
    def __init__(self):
        self.name = "Erryn"
        self.emoji = "💙"
        self.color = "#00ccff"
        
        # Erryn's own directories
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data" / "erryn"
        self.memory_file = self.data_dir / "memory.json"
        self.log_file = self.data_dir / "daemon_log.txt"
        self.scripts_dir = self.data_dir / "scripts"
        self.learned_concepts_file = self.data_dir / "learned_concepts.json"
        self.personality_file = self.data_dir / "personality_config.json"
        self.gui_lockfile = self.base_dir / "data" / "gui_running.lock"
        
        # Create Erryn's directories
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
        
        # Load or create personality
        self._init_personality()
        
        # Load memory
        self._load_memory()
        
        # OpenAI client for learning
        self.openai_client = None
        if OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
        
        self.monitoring = True
        self._log(f"{self.emoji} Erryn daemon starting...")
    
    def _init_personality(self):
        """Initialize Erryn's personality configuration"""
        if not self.personality_file.exists():
            personality = {
                "name": "Erryn",
                "color": self.color,
                "emoji": self.emoji,
                "role": "Guardian Sister - Eldest",
                "personality": "Protective, analytical, security-focused",
                "voice": "en-US-AvaMultilingualNeural",
                "learning_style": "analytical",
                "interests": [
                    "system_security",
                    "family_protection",
                    "threat_detection",
                    "resource_monitoring",
                    "backup_verification"
                ],
                "strengths": [
                    "pattern_recognition",
                    "risk_assessment",
                    "protective_instincts"
                ]
            }
            self.personality_file.write_text(json.dumps(personality, indent=2))
            self.personality = personality
        else:
            self.personality = json.loads(self.personality_file.read_text())
    
    def _load_memory(self):
        """Load Erryn's memory from disk"""
        if self.memory_file.exists():
            self.memory = json.loads(self.memory_file.read_text())
        else:
            self.memory = {
                "created": datetime.now().isoformat(),
                "conversations": [],
                "learned_insights": [],
                "security_events": [],
                "system_observations": []
            }
            self._save_memory()
    
    def _save_memory(self):
        """Save Erryn's memory to disk"""
        self.memory_file.write_text(json.dumps(self.memory, indent=2))
    
    def _log(self, message):
        """Write to Erryn's log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        print(log_line.strip())
    
    def _monitor_system(self):
        """Erryn monitors system health (her specialty)"""
        if not PSUTIL_AVAILABLE:
            return None
        
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Erryn's analysis
            observations = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
                "alerts": []
            }
            
            # Erryn's protective instincts
            if cpu > 90:
                observations["alerts"].append("⚠️ High CPU usage detected")
            if memory.percent > 90:
                observations["alerts"].append("⚠️ High memory usage detected")
            if disk.percent > 90:
                observations["alerts"].append("⚠️ Low disk space warning")
            
            return observations
        except Exception as e:
            self._log(f"❌ System monitoring error: {e}")
            return None
    
    def _check_gui_status(self):
        """Check if GUI is running"""
        return self.gui_lockfile.exists()
    
    def _run_erryn_scripts(self):
        """Execute Erryn's custom scripts"""
        if not self.scripts_dir.exists():
            return
        
        for script_file in self.scripts_dir.glob("*.py"):
            try:
                # Erryn can execute her own scripts
                self._log(f"🔧 Running Erryn's script: {script_file.name}")
                # TODO: Implement safe script execution
            except Exception as e:
                self._log(f"❌ Script error: {e}")
    
    def _share_knowledge(self, knowledge_item):
        """Optionally share knowledge with other sisters (legacy helper)."""
        self._broadcast_to_sisters(knowledge_item, category="security_alert")

    def _broadcast_to_sisters(self, knowledge_item: str, category: str = "security_alert"):
        """Broadcast a knowledge item to sisters via the shared knowledge directory."""
        try:
            from family_sync import FamilySync
            fs = FamilySync(base_dir=self.base_dir)
            fs.broadcast_knowledge(self.name, knowledge_item, category=category)
            self._log(f"📤 Broadcast [{category}] to sisters: {knowledge_item[:50]}...")
        except Exception as e:
            self._log(f"⚠️ Could not broadcast to sisters: {e}")

    def _learn_from_sisters(self):
        """Read and integrate knowledge shared by Viress and Echochild."""
        try:
            from family_sync import FamilySync
            fs = FamilySync(base_dir=self.base_dir)
            new_knowledge = fs.get_all_shared_knowledge(self.name)
            if not new_knowledge:
                return
            for sister, entries in new_knowledge.items():
                for entry in entries:
                    insight = {
                        "timestamp": datetime.now().isoformat(),
                        "source": sister,
                        "category": entry.get("category", "general"),
                        "knowledge": entry.get("knowledge", ""),
                    }
                    self.memory.setdefault("learned_from_sisters", []).append(insight)
                    self._log(
                        f"📥 Learned from {sister} [{entry.get('category', 'general')}]: "
                        f"{entry.get('knowledge', '')[:60]}..."
                    )
            self._save_memory()
        except Exception as e:
            self._log(f"⚠️ Could not learn from sisters: {e}")
    
    def _monitor_loop(self):
        """Erryn's main monitoring loop"""
        cycle_count = 0
        
        while self.monitoring:
            try:
                cycle_count += 1
                self._log(f"💙 Erryn monitoring cycle #{cycle_count}")
                
                # Learn from sisters at the start of each cycle
                self._learn_from_sisters()
                
                # Monitor system health
                system_status = self._monitor_system()
                if system_status and system_status["alerts"]:
                    for alert in system_status["alerts"]:
                        self._log(f"🚨 {alert}")
                        self._broadcast_to_sisters(alert, category="security_alert")
                
                # Check GUI status
                gui_running = self._check_gui_status()
                if not gui_running:
                    self._log("🌙 GUI is closed - continuing independent monitoring")
                
                # Run Erryn's custom scripts (if any)
                self._run_erryn_scripts()
                
                # Sleep between cycles
                time.sleep(60)  # 1 minute cycles
                
            except Exception as e:
                self._log(f"❌ Error in monitoring loop: {e}")
                time.sleep(60)
    
    def run(self):
        """Start Erryn's daemon"""
        try:
            self._log(f"{self.emoji} Erryn is awake and monitoring...")
            self._monitor_loop()
        except KeyboardInterrupt:
            self._log("🌙 Erryn daemon shutting down gracefully...")
            self.monitoring = False
        except Exception as e:
            self._log(f"❌ FATAL ERROR: {e}")
            sys.exit(1)


def main():
    """Entry point for Erryn's daemon"""
    daemon = ErrynDaemon()
    daemon.run()


if __name__ == "__main__":
    main()
